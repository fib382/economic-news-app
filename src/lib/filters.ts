import type { Category, Importance, NewsItem } from "./types";

export const categories: Category[] = [
  "イラン・中東情勢",
  "要人発言",
  "FRB",
  "米国経済",
  "為替",
  "債券",
  "株式",
  "原油・エネルギー",
  "経済指標",
  "その他"
];

export const importances: Importance[] = ["A", "B", "C"];

export interface NewsFilters {
  category: Category | "すべて";
  importance: Importance | "すべて";
  query: string;
}

export function filterNews(items: NewsItem[], filters: NewsFilters): NewsItem[] {
  const query = filters.query.trim().toLowerCase();
  return items
    .filter((item) => filters.category === "すべて" || item.category === filters.category)
    .filter((item) => filters.importance === "すべて" || item.importance === filters.importance)
    .filter((item) => {
      if (!query) return true;
      return [item.title, item.summary, item.source, item.category, ...item.tags]
        .join(" ")
        .toLowerCase()
        .includes(query);
    })
    .sort((a, b) => new Date(b.published_at).getTime() - new Date(a.published_at).getTime());
}
