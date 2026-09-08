import { Controller, Get, Param, NotFoundException } from '@nestjs/common';
import { BuyersService } from './buyers.service';

@Controller('buyers')
export class BuyersController {
  constructor(private readonly buyersService: BuyersService) {}

  @Get()
  async findAll() {
    return await this.buyersService.findAll();
  }

  @Get(':id')
  async findOne(@Param('id') id: string) {
    const buyer = await this.buyersService.findOne(id);
    if (!buyer) {
      throw new NotFoundException(`Buyer with ID ${id} not found`);
    }
    return buyer;
  }
}
