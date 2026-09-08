import { IsOptional, IsString, IsIn } from 'class-validator';

export class TranscribeDto {
  @IsOptional()
  @IsString()
  @IsIn(['en', 'hi', 'mr'])
  language?: string;
}
