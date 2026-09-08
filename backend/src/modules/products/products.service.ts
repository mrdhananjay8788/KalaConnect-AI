import { Injectable, NotFoundException, ForbiddenException, BadRequestException, ConflictException } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { CreateProductDto } from './dto/create-product.dto';
import { UpdateProductDto } from './dto/update-product.dto';
import { ProductStatus } from '@prisma/client';

@Injectable()
export class ProductsService {
  constructor(private readonly prisma: PrismaService) {}

  private generateSlug(name: string): string {
    return name
      .toLowerCase()
      .trim()
      .replace(/[^\w\s-]/g, '')
      .replace(/[\s_-]+/g, '-')
      .replace(/^-+|-+$/g, '');
  }

  private async getUniqueSlug(name: string, excludeId?: string): Promise<string> {
    let slug = this.generateSlug(name);
    let isUnique = false;
    let attempt = 0;
    
    while (!isUnique) {
      const existing = await this.prisma.product.findFirst({
        where: {
          slug,
          id: excludeId ? { not: excludeId } : undefined,
        },
      });
      
      if (!existing) {
        isUnique = true;
      } else {
        attempt++;
        slug = `${this.generateSlug(name)}-${Math.floor(Math.random() * 10000)}-${attempt}`;
      }
    }
    return slug;
  }

  async create(userId: string, createProductDto: CreateProductDto) {
    const artisan = await this.prisma.artisan.findUnique({
      where: { userId },
    });

    if (!artisan) {
      throw new ForbiddenException('Only verified artisans can create products');
    }

    const category = await this.prisma.category.findUnique({
      where: { id: createProductDto.categoryId },
    });

    if (!category || !category.active) {
      throw new BadRequestException('Invalid or inactive category');
    }

    const slug = await this.getUniqueSlug(createProductDto.name);

    return await this.prisma.$transaction(async (tx) => {
      const product = await tx.product.create({
        data: {
          artisanId: artisan.id,
          categoryId: createProductDto.categoryId,
          name: createProductDto.name,
          slug,
          description: createProductDto.description,
          material: createProductDto.material,
          price: createProductDto.price,
          currency: createProductDto.currency ?? 'INR',
          stockQuantity: createProductDto.stockQuantity ?? 0,
          status: ProductStatus.DRAFT,
          featured: false,
        },
      });

      if (createProductDto.imageUrls && createProductDto.imageUrls.length > 0) {
        await tx.productImage.createMany({
          data: createProductDto.imageUrls.map((url, index) => ({
            productId: product.id,
            url,
            sortOrder: index,
          })),
        });
      }

      return await tx.product.findUnique({
        where: { id: product.id },
        include: { images: true, category: true },
      });
    });
  }

  async findAll(query: any, userRole?: string) {
    const { categoryId, artisanId, status, search, page = 1, limit = 10 } = query;
    const pageNum = Number(page);
    const limitNum = Number(limit);
    const skip = (pageNum - 1) * limitNum;

    const where: any = {};

    if (categoryId) where.categoryId = categoryId;
    if (artisanId) where.artisanId = artisanId;
    
    if (search) {
      where.OR = [
        { name: { contains: search, mode: 'insensitive' } },
        { description: { contains: search, mode: 'insensitive' } },
      ];
    }

    if (!userRole || userRole === 'BUYER' || !status) {
      where.status = ProductStatus.APPROVED;
    } else if (status) {
      where.status = status;
    }

    const [total, data] = await Promise.all([
      this.prisma.product.count({ where }),
      this.prisma.product.findMany({
        where,
        include: {
          images: true,
          category: true,
          artisan: {
            include: {
              user: {
                select: { fullName: true }
              }
            }
          }
        },
        skip,
        take: limitNum,
        orderBy: { createdAt: 'desc' },
      })
    ]);

    return {
      data,
      pagination: {
        page: pageNum,
        limit: limitNum,
        total,
        totalPages: Math.ceil(total / limitNum) || 1,
      }
    };
  }

  async findMyProducts(userId: string, query: any) {
    const artisan = await this.prisma.artisan.findUnique({
      where: { userId },
    });

    if (!artisan) {
      throw new ForbiddenException('Only artisans can access their products');
    }

    const { page = 1, limit = 10 } = query;
    const pageNum = Number(page);
    const limitNum = Number(limit);
    const skip = (pageNum - 1) * limitNum;

    const where = { artisanId: artisan.id };

    const [total, data] = await Promise.all([
      this.prisma.product.count({ where }),
      this.prisma.product.findMany({
        where,
        include: { images: true, category: true },
        skip,
        take: limitNum,
        orderBy: { createdAt: 'desc' },
      })
    ]);

    return {
      data,
      pagination: {
        page: pageNum,
        limit: limitNum,
        total,
        totalPages: Math.ceil(total / limitNum) || 1,
      }
    };
  }

  async findOne(id: string, userId?: string, userRole?: string) {
    const product = await this.prisma.product.findUnique({
      where: { id },
      include: {
        images: true,
        category: true,
        artisan: {
          include: {
            user: { select: { fullName: true } }
          }
        }
      },
    });

    if (!product) {
      throw new NotFoundException('Product not found');
    }

    if (product.status !== ProductStatus.APPROVED) {
      if (!userId) {
        throw new NotFoundException('Product not found');
      }

      if (userRole === 'ARTISAN') {
        const artisan = await this.prisma.artisan.findUnique({ where: { userId } });
        if (!artisan || artisan.id !== product.artisanId) {
          throw new NotFoundException('Product not found');
        }
      } else if (userRole !== 'ADMIN') {
        throw new NotFoundException('Product not found');
      }
    }

    return product;
  }

  async update(id: string, userId: string, updateProductDto: UpdateProductDto) {
    const artisan = await this.prisma.artisan.findUnique({ where: { userId } });
    if (!artisan) {
      throw new ForbiddenException('Only artisans can edit products');
    }

    const product = await this.prisma.product.findUnique({ where: { id } });
    if (!product) {
      throw new NotFoundException('Product not found');
    }

    if (product.artisanId !== artisan.id) {
      throw new ForbiddenException('You do not own this product');
    }

    if (updateProductDto.categoryId) {
      const category = await this.prisma.category.findUnique({ where: { id: updateProductDto.categoryId } });
      if (!category || !category.active) {
        throw new BadRequestException('Invalid or inactive category');
      }
    }

    const updateData: any = { ...updateProductDto };
    delete updateData.imageUrls;

    if (updateData.name && updateData.name !== product.name) {
      updateData.slug = await this.getUniqueSlug(updateData.name, id);
    }

    return await this.prisma.$transaction(async (tx) => {
      const updatedProduct = await tx.product.update({
        where: { id },
        data: updateData,
      });

      if (updateProductDto.imageUrls) {
        await tx.productImage.deleteMany({ where: { productId: id } });
        if (updateProductDto.imageUrls.length > 0) {
          await tx.productImage.createMany({
            data: updateProductDto.imageUrls.map((url, index) => ({
              productId: id,
              url,
              sortOrder: index,
            })),
          });
        }
      }

      return await tx.product.findUnique({
        where: { id },
        include: { images: true, category: true },
      });
    });
  }

  async remove(id: string, userId: string) {
    const artisan = await this.prisma.artisan.findUnique({ where: { userId } });
    if (!artisan) {
      throw new ForbiddenException('Only artisans can delete products');
    }

    const product = await this.prisma.product.findUnique({ where: { id } });
    if (!product) {
      throw new NotFoundException('Product not found');
    }

    if (product.artisanId !== artisan.id) {
      throw new ForbiddenException('You do not own this product');
    }

    await this.prisma.product.delete({ where: { id } });
    
    return { message: 'Product deleted successfully' };
  }
}
