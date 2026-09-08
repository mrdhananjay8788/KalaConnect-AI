import { 
  Controller, 
  Post, 
  Body, 
  UseGuards, 
  UseInterceptors, 
  UploadedFile,
  BadRequestException
} from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { VoiceService } from './voice.service';
import { TranscribeDto } from './dto/transcribe.dto';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { RolesGuard } from '../auth/guards/roles.guard';
import { Roles } from '../auth/decorators/roles.decorator';
import { UserRole } from '@prisma/client';

@Controller('voice')
export class VoiceController {
  constructor(private readonly voiceService: VoiceService) {}

  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(UserRole.ARTISAN)
  @Post('transcribe')
  @UseInterceptors(
    FileInterceptor('audio', {
      limits: {
        fileSize: 10 * 1024 * 1024, // 10MB limit
      },
      fileFilter: (req, file, cb) => {
        // Safe memory processing, just validating MIME types
        const allowedMimeTypes = [
          'audio/mpeg',
          'audio/mp3',
          'audio/wav',
          'audio/x-wav',
          'audio/webm',
          'audio/mp4',
          'audio/m4a',
        ];
        
        if (!allowedMimeTypes.includes(file.mimetype)) {
          return cb(new BadRequestException('Unsupported audio format'), false);
        }
        cb(null, true);
      }
    })
  )
  async transcribe(
    @UploadedFile() file: Express.Multer.File,
    @Body() transcribeDto: TranscribeDto,
  ) {
    if (!file) {
      throw new BadRequestException('Audio file is required');
    }
    
    return this.voiceService.transcribeAudio(file, transcribeDto);
  }
}
