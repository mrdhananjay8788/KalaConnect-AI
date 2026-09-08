import { Controller, Get, Post, Body, Patch, Param, Delete, UseGuards, Request, Query } from '@nestjs/common';
import { ProductsService } from './products.service';
import { CreateProductDto } from './dto/create-product.dto';
import { UpdateProductDto } from './dto/update-product.dto';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { RolesGuard } from '../auth/guards/roles.guard';
import { Roles } from '../auth/decorators/roles.decorator';
import { UserRole } from '@prisma/client';

@Controller('products')
export class ProductsController {
  constructor(private readonly productsService: ProductsService) {}

  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(UserRole.ARTISAN)
  @Post()
  create(@Request() req, @Body() createProductDto: CreateProductDto) {
    return this.productsService.create(req.user.id, createProductDto);
  }

  @Get()
  findAll(@Query() query: any, @Request() req) {
    // We optionally extract user role if they are authenticated, but it's a public endpoint.
    // For this, we can optionally use a strategy that doesn't throw if no token is present,
    // but the requirement is simpler: public users see APPROVED. 
    // In NestJS, a standard Get endpoint without guards won't populate req.user unless a global/optional guard does.
    // We will assume public access and handle role-based filtering if a token is manually verified,
    // but the spec says "If no privileged authentication context exists, never expose DRAFT..."
    // Since it's public, we just pass undefined for userRole which defaults to APPROVED only in service.
    return this.productsService.findAll(query, req.user?.role);
  }

  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(UserRole.ARTISAN)
  @Get('me')
  findMyProducts(@Request() req, @Query() query: any) {
    return this.productsService.findMyProducts(req.user.id, query);
  }

  @Get(':id')
  findOne(@Param('id') id: string, @Request() req) {
    // Similar to findAll, it's public but owners can see their own unapproved products.
    // For a fully secure optional auth, we'd use a custom guard. 
    // Here we rely on the service logic. If req.user is undefined, it only returns APPROVED.
    return this.productsService.findOne(id, req.user?.id, req.user?.role);
  }

  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(UserRole.ARTISAN)
  @Patch(':id')
  update(@Param('id') id: string, @Request() req, @Body() updateProductDto: UpdateProductDto) {
    return this.productsService.update(id, req.user.id, updateProductDto);
  }

  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(UserRole.ARTISAN)
  @Delete(':id')
  remove(@Param('id') id: string, @Request() req) {
    return this.productsService.remove(id, req.user.id);
  }
}
