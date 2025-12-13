export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface ProductPriceByChain {
  chain_id: number;
  chain_name: string;
  price: number;
}

export interface ProductSummary {
  id: number;
  code: string;
  name: string;
  unit: string;
  prices: ProductPriceByChain[];
}

export interface HistoricalPricePoint {
  date: string;
  chain_id: number;
  chain_name: string;
  price: number;
}

export interface ProductDetail {
  id: number;
  code: string;
  name: string;
  unit: string;
  category: string | null;
  history: HistoricalPricePoint[];
}

export interface DailyIndexPoint {
  date: string;
  index_value: number;
}


