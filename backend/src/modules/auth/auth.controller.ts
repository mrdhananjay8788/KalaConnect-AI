import { Controller, Post, Body, Get, UseGuards, Request } from '@nestjs/common';
import { AuthService } from './auth.service';
import { RegisterDto } from './dto/register.dto';
import { LoginDto } from './dto/login.dto';
import { JwtAuthGuard } from './guards/jwt-auth.guard';
import { PrismaService } from '../../prisma/prisma.service';
import { UserRole } from '@prisma/client';

@Controller('auth')
export class AuthController {
  constructor(
    private readonly authService: AuthService,
    private readonly prisma: PrismaService,
  ) {}

  @Post('register')
  async register(@Body() registerDto: RegisterDto) {
    return await this.authService.register(registerDto);
  }

  @Post('login')
  async login(@Body() loginDto: LoginDto) {
    return await this.authService.login(loginDto);
  }

  @UseGuards(JwtAuthGuard)
  @Get('me')
  async getCurrentUser(@Request() req) {
    const userId = req.user.id;
    const userRole = req.user.role;

    const selectOptions: any = {
      id: true,
      fullName: true,
      email: true,
      phone: true,
      role: true,
      status: true,
      createdAt: true,
      updatedAt: true,
    };

    if (userRole === UserRole.ARTISAN) {
      selectOptions.artisan = true;
    } else if (userRole === UserRole.BUYER) {
      selectOptions.buyer = true;
    }

    const user = await this.prisma.user.findUnique({
      where: { id: userId },
      select: selectOptions,
    });

    return user;
  }
}
