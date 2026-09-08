import { Controller, Get, Param, NotFoundException } from '@nestjs/common';
import { ArtisansService } from './artisans.service';

@Controller('artisans')
export class ArtisansController {
  constructor(private readonly artisansService: ArtisansService) {}

  @Get()
  async findAll() {
    return await this.artisansService.findAll();
  }

  @Get(':id')
  async findOne(@Param('id') id: string) {
    const artisan = await this.artisansService.findOne(id);
    if (!artisan) {
      throw new NotFoundException(`Artisan with ID ${id} not found`);
    }
    return artisan;
  }
}
