import { Controller, Post, Body, UseGuards } from '@nestjs/common';
import { AiService } from './ai.service';
import { GenerateCatalogDto } from './dto/generate-catalog.dto';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { RolesGuard } from '../auth/guards/roles.guard';
import { Roles } from '../auth/decorators/roles.decorator';
import { UserRole } from '@prisma/client';

@Controller('ai')
export class AiController {
  constructor(private readonly aiService: AiService) {}

  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(UserRole.ARTISAN)
  @Post('catalog/generate')
  async generateCatalog(@Body() generateCatalogDto: GenerateCatalogDto) {
    return this.aiService.generateCatalogSuggestions(generateCatalogDto);
  }
}
