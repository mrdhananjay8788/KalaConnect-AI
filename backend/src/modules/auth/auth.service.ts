import { Injectable, ConflictException, UnauthorizedException, BadRequestException } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { JwtService } from '@nestjs/jwt';
import { RegisterDto } from './dto/register.dto';
import { LoginDto } from './dto/login.dto';
import * as bcrypt from 'bcryptjs';
import { UserRole } from '@prisma/client';

@Injectable()
export class AuthService {
  constructor(
    private prisma: PrismaService,
    private jwtService: JwtService,
  ) {}

  async register(registerDto: RegisterDto) {
    const { fullName, email, phone, password, role } = registerDto;

    if (role === UserRole.ADMIN) {
      throw new BadRequestException('Cannot register as ADMIN through public API');
    }

    const existingUser = await this.prisma.user.findFirst({
      where: {
        OR: [
          { email },
          phone ? { phone } : undefined,
        ].filter(Boolean) as any,
      },
    });

    if (existingUser) {
      if (existingUser.email === email) {
        throw new ConflictException('Email is already registered');
      }
      if (existingUser.phone === phone) {
        throw new ConflictException('Phone number is already registered');
      }
    }

    const hashedPassword = await bcrypt.hash(password, 10);

    const result = await this.prisma.$transaction(async (prisma) => {
      const user = await prisma.user.create({
        data: {
          fullName,
          email,
          phone,
          password: hashedPassword,
          role,
        },
      });

      if (role === UserRole.ARTISAN) {
        await prisma.artisan.create({
          data: {
            userId: user.id,
          },
        });
      } else if (role === UserRole.BUYER) {
        await prisma.buyer.create({
          data: {
            userId: user.id,
          },
        });
      }

      return user;
    });

    const payload = { sub: result.id, email: result.email, role: result.role };
    const accessToken = this.jwtService.sign(payload);

    const safeUser = {
      id: result.id,
      fullName: result.fullName,
      email: result.email,
      role: result.role,
    };

    return {
      message: 'Registration successful',
      user: safeUser,
      accessToken,
    };
  }

  async login(loginDto: LoginDto) {
    const { email, password } = loginDto;

    const user = await this.prisma.user.findUnique({
      where: { email },
    });

    if (!user) {
      throw new UnauthorizedException('Invalid credentials');
    }

    if (user.status !== 'ACTIVE') {
      throw new UnauthorizedException('User is inactive or suspended');
    }

    const isPasswordValid = await bcrypt.compare(password, user.password);

    if (!isPasswordValid) {
      throw new UnauthorizedException('Invalid credentials');
    }

    const payload = { sub: user.id, email: user.email, role: user.role };
    const accessToken = this.jwtService.sign(payload);

    const safeUser = {
      id: user.id,
      fullName: user.fullName,
      email: user.email,
      role: user.role,
      status: user.status,
    };

    return {
      message: 'Login successful',
      accessToken,
      user: safeUser,
    };
  }
}
