import { Injectable, InternalServerErrorException, ServiceUnavailableException, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { GoogleGenAI } from '@google/genai';
import { GenerateCatalogDto } from './dto/generate-catalog.dto';
import { CatalogSuggestion } from './interfaces/catalog-suggestion.interface';

@Injectable()
export class AiService {
  private ai: GoogleGenAI | null = null;
  private model: string;
  private readonly logger = new Logger(AiService.name);

  constructor(private configService: ConfigService) {
    const apiKey = this.configService.get<string>('GEMINI_API_KEY');
    this.model = this.configService.get<string>('AI_MODEL') || 'gemini-1.5-flash';
    
    if (apiKey) {
      this.ai = new GoogleGenAI({ apiKey });
    }
  }

  async generateCatalogSuggestions(dto: GenerateCatalogDto): Promise<CatalogSuggestion> {
    if (!this.ai) {
      throw new InternalServerErrorException('AI provider is not configured. Missing API Key.');
    }

    const { name, basicDescription, material, craftType, language } = dto;
    
    const targetLanguage = language === 'hi' ? 'Hindi' : language === 'mr' ? 'Marathi' : 'English';

    const prompt = `
      Act as an AI Smart Catalog Assistant for an artisanal marketplace.
      Your task is to improve and structure the following product information into a professional, marketplace-ready format.
      
      Input Data:
      Name: ${name}
      Basic Description: ${basicDescription || 'N/A'}
      Material: ${material || 'N/A'}
      Craft Type: ${craftType || 'N/A'}
      Target Language: ${targetLanguage}
      
      Rules:
      1. Generate accurate product catalog information in ${targetLanguage}.
      2. Improve grammar and clarity.
      3. Preserve the Artisan's original meaning.
      4. Never invent certifications.
      5. Never claim a product is officially certified unless stated.
      6. Never invent a geographical indication.
      7. Never make false historical or cultural claims.
      8. Never claim "100% organic" unless explicitly supplied by the user.
      9. Avoid misleading marketing claims.
      10. Keep descriptions useful for an online marketplace.
      11. ONLY output valid, raw JSON exactly matching this structure, with no markdown formatting, no backticks, and no extra text:
      
      {
        "name": "Improved Product Name",
        "description": "Professional product description",
        "shortDescription": "Short marketplace description",
        "suggestedMaterial": "Cotton",
        "suggestedCraftType": "Handmade Textile",
        "keywords": ["handmade", "cotton"],
        "suggestedCategory": "Textiles",
        "language": "${language}"
      }
    `;

    try {
      const response = await this.ai.models.generateContent({
        model: this.model,
        contents: prompt,
      });

      let text = response.text || '';
      
      // Attempt to clean up markdown code blocks if the model ignores the "no backticks" instruction
      text = text.replace(/^```json\s*/i, '').replace(/\s*```$/i, '').trim();

      let parsed: any;
      try {
        parsed = JSON.parse(text);
      } catch (parseError) {
        this.logger.error('Failed to parse AI response', text);
        throw new InternalServerErrorException('Failed to parse AI response as JSON');
      }

      // Validate structure safely
      if (!parsed.name || typeof parsed.name !== 'string') throw new InternalServerErrorException('Invalid AI response: Missing name');
      if (typeof parsed.description !== 'string') throw new InternalServerErrorException('Invalid AI response: Missing description');
      
      const suggestion: CatalogSuggestion = {
        name: parsed.name,
        description: parsed.description,
        shortDescription: parsed.shortDescription || '',
        suggestedMaterial: parsed.suggestedMaterial || null,
        suggestedCraftType: parsed.suggestedCraftType || null,
        keywords: Array.isArray(parsed.keywords) ? parsed.keywords : [],
        suggestedCategory: parsed.suggestedCategory || null,
        language: parsed.language || language || 'en',
      };

      return suggestion;

    } catch (error: any) {
      this.logger.error('AI Generation Error', error.message);
      if (error instanceof InternalServerErrorException) {
        throw error;
      }
      throw new ServiceUnavailableException('AI provider is currently unavailable');
    }
  }
}
