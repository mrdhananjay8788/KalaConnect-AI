import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';

@Injectable()
export class BuyersService {
  constructor(private readonly prisma: PrismaService) {}

  async findAll() {
    return await this.prisma.buyer.findMany();
  }

  async findOne(id: string) {
    return await this.prisma.buyer.findUnique({
      where: { id },
    });
  }
}
