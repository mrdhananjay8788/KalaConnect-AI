import { Injectable, Logger } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';

@Injectable()
export class HealthService {
  private readonly logger = new Logger(HealthService.name);

  constructor(private readonly prisma: PrismaService) {}

  async checkHealth() {
    let databaseStatus = 'disconnected';
    
    try {
      // Simple query to verify database connection
      await this.prisma.$queryRaw`SELECT 1`;
      databaseStatus = 'connected';
    } catch (error) {
      this.logger.error('Database connection failed during health check', error);
      databaseStatus = 'error';
    }

    return {
      status: 'ok',
      message: 'KalaConnect-AI Backend is running',
      database: databaseStatus,
    };
  }
}
