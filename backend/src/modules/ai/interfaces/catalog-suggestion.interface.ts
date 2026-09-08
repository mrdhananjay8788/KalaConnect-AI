export interface CatalogSuggestion {
  name: string;
  description: string;
  shortDescription: string;
  suggestedMaterial: string | null;
  suggestedCraftType: string | null;
  keywords: string[];
  suggestedCategory: string | null;
  language: string;
}
