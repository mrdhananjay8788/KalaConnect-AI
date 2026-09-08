import { IsString, IsNotEmpty, IsOptional, IsIn } from 'class-validator';

export class GenerateCatalogDto {
  @IsNotEmpty()
  @IsString()
  name: string;

  @IsOptional()
  @IsString()
  basicDescription?: string;

  @IsOptional()
  @IsString()
  material?: string;

  @IsOptional()
  @IsString()
  craftType?: string;

  @IsOptional()
  @IsString()
  @IsIn(['en', 'hi', 'mr'])
  language?: string = 'en';
}
