export type Category =
  | "イラン・中東情勢"
  | "要人発言"
  | "FRB"
  | "米国経済"
  | "為替"
  | "債券"
  | "株式"
  | "原油・エネルギー"
  | "経済指標"
  | "その他";

export type Importance = "A" | "B" | "C";

export interface MarketImpact {
  fx: string;
  bonds: string;
  stocks: string;
  commodities: string;
}

export interface NewsItem {
  id: string;
  source: string;
  source_type: string;
  title: string;
  summary: string;
  url: string;
  published_at: string;
  fetched_at: string;
  language: string;
  country?: string;
  category: Category;
  importance: Importance;
  confidence: "low" | "medium" | "high";
  market_impact: MarketImpact;
  tags: string[];
}

export interface NewsItemsPayload {
  generated_at: string;
  items: NewsItem[];
}

export interface MarketSnapshotItem {
  symbol: string;
  name: string;
  source: string;
  value: number | null;
  unit: string;
  date: string | null;
  change_1d: number | null;
  category: Category;
}

export interface MarketSnapshotPayload {
  generated_at: string;
  items: MarketSnapshotItem[];
}

export interface DailyReportSection {
  title: string;
  summary: string;
  importance: Importance;
  source_item_ids: string[];
}

export interface DailyReportPayload {
  date: string;
  generated_at: string;
  headline: string;
  executive_summary: string;
  sections: DailyReportSection[];
  watch_points: string[];
}

export interface SourceInfo {
  name: string;
  category: string;
  method: string;
  priority: Importance;
  url: string;
  status: "active" | "optional" | "planned" | "skipped";
  notes?: string;
}

export interface SourcesPayload {
  generated_at: string;
  items: SourceInfo[];
}
