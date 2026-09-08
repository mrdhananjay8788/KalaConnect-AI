import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import appConfig from './config/app.config';
import databaseConfig from './config/database.config';
import { PrismaModule } from './prisma/prisma.module';
import { HealthModule } from './modules/health/health.module';
import { UsersModule } from './modules/users/users.module';
import { ArtisansModule } from './modules/artisans/artisans.module';
import { BuyersModule } from './modules/buyers/buyers.module';
import { CategoriesModule } from './modules/categories/categories.module';
import { AuthModule } from './modules/auth/auth.module';
import { ProductsModule } from './modules/products/products.module';
import { AiModule } from './modules/ai/ai.module';
import { VoiceModule } from './modules/voice/voice.module';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      load: [appConfig, databaseConfig],
    }),
    PrismaModule,
    HealthModule,
    UsersModule,
    ArtisansModule,
    BuyersModule,
    CategoriesModule,
    AuthModule,
    ProductsModule,
    AiModule,
    VoiceModule,
  ],
  controllers: [],
  providers: [],
})
export class AppModule {}
