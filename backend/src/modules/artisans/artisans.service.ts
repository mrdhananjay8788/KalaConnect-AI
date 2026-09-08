import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';

@Injectable()
export class ArtisansService {
  constructor(private readonly prisma: PrismaService) {}

  async findAll() {
    return await this.prisma.artisan.findMany();
  }

  async findOne(id: string) {
    return await this.prisma.artisan.findUnique({
      where: { id },
    });
  }
}
