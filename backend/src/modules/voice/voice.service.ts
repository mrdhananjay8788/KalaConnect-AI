import { Injectable, InternalServerErrorException, ServiceUnavailableException, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { GoogleGenAI } from '@google/genai';
import { TranscriptionResult } from './interfaces/transcription-result.interface';
import { TranscribeDto } from './dto/transcribe.dto';

@Injectable()
export class VoiceService {
  private ai: GoogleGenAI | null = null;
  private model: string;
  private readonly logger = new Logger(VoiceService.name);

  constructor(private configService: ConfigService) {
    // Reusing the Gemini configuration for speech-to-text as requested
    const apiKey = this.configService.get<string>('SPEECH_API_KEY') || this.configService.get<string>('GEMINI_API_KEY');
    this.model = this.configService.get<string>('SPEECH_MODEL') || this.configService.get<string>('AI_MODEL') || 'gemini-1.5-flash';
    
    if (apiKey) {
      this.ai = new GoogleGenAI({ apiKey });
    }
  }

  async transcribeAudio(file: Express.Multer.File, dto: TranscribeDto): Promise<TranscriptionResult> {
    if (!this.ai) {
      throw new InternalServerErrorException('Speech provider is not configured. Missing API Key.');
    }

    const { language } = dto;
    const targetLanguage = language === 'hi' ? 'Hindi' : language === 'mr' ? 'Marathi' : language === 'en' ? 'English' : 'its original language';

    // Convert audio buffer to base64 for Gemini inlineData
    const base64Audio = file.buffer.toString('base64');

    const prompt = `Please transcribe this audio exactly as spoken in ${targetLanguage}. Return ONLY the transcript text without any introductory text, markdown, or quotation marks.`;

    try {
      const response = await this.ai.models.generateContent({
        model: this.model,
        contents: [
          {
            inlineData: {
              data: base64Audio,
              mimeType: file.mimetype,
            },
          },
          prompt,
        ],
      });

      const text = (response.text || '').trim();
      
      if (!text) {
        throw new InternalServerErrorException('Empty transcription returned by the provider.');
      }

      return {
        success: true,
        transcript: text,
        language: language || 'en', // Defaulting to English if auto-detect isn't explicitly passed back
      };

    } catch (error: any) {
      this.logger.error('Transcription Error', error.message);
      if (error instanceof InternalServerErrorException) {
        throw error;
      }
      throw new ServiceUnavailableException('Speech provider is currently unavailable or transcription failed.');
    }
  }
}
