import { ExternalLink, Search } from "lucide-react";
import { useMemo, useState } from "react";
import { categories, filterNews, importances, type NewsFilters } from "../lib/filters";
import { formatDateTime } from "../lib/format";
import type { NewsItem } from "../lib/types";
import { ImportanceBadge } from "./ImportanceBadge";
import { SourceBadge } from "./SourceBadge";

export function NewsList({ items }: { items: NewsItem[] }) {
  const [filters, setFilters] = useState<NewsFilters>({
    category: "すべて",
    importance: "すべて",
    query: ""
  });
  const filtered = useMemo(() => filterNews(items, filters), [items, filters]);

  return (
    <section id="news" className="space-y-4">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h2 className="text-lg font-semibold text-ink">ニュース一覧</h2>
          <p className="text-sm text-slate-600">{filtered.length}件 / 全{items.length}件</p>
        </div>
        <div className="grid gap-2 sm:grid-cols-[180px_120px_240px]">
          <select
            className="h-10 rounded border border-line bg-white px-3 text-sm"
            value={filters.category}
            onChange={(event) => setFilters((current) => ({ ...current, category: event.target.value as NewsFilters["category"] }))}
          >
            <option value="すべて">すべてのカテゴリ</option>
            {categories.map((category) => (
              <option key={category} value={category}>{category}</option>
            ))}
          </select>
          <select
            className="h-10 rounded border border-line bg-white px-3 text-sm"
            value={filters.importance}
            onChange={(event) => setFilters((current) => ({ ...current, importance: event.target.value as NewsFilters["importance"] }))}
          >
            <option value="すべて">重要度すべて</option>
            {importances.map((importance) => (
              <option key={importance} value={importance}>重要度{importance}</option>
            ))}
          </select>
          <label className="relative block">
            <Search className="pointer-events-none absolute left-3 top-2.5 h-5 w-5 text-slate-400" aria-hidden="true" />
            <input
              className="h-10 w-full rounded border border-line bg-white pl-10 pr-3 text-sm"
              placeholder="キーワード検索"
              value={filters.query}
              onChange={(event) => setFilters((current) => ({ ...current, query: event.target.value }))}
            />
          </label>
        </div>
      </div>
      <div className="grid gap-3">
        {filtered.map((item) => (
          <article key={item.id} className={`rounded-lg border bg-white p-4 shadow-subtle ${item.importance === "A" ? "border-risk" : "border-line"}`}>
            <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
              <div className="space-y-2">
                <div className="flex flex-wrap items-center gap-2">
                  <ImportanceBadge value={item.importance} />
                  <SourceBadge source={item.source} />
                  <span className="rounded border border-line bg-panel px-2 py-1 text-xs text-slate-600">{item.category}</span>
                  <span className="text-xs text-slate-500">{formatDateTime(item.published_at)}</span>
                </div>
                <h3 className="text-base font-bold text-ink">{item.title}</h3>
              </div>
              <a
                href={item.url}
                target="_blank"
                rel="noreferrer"
                className="inline-flex h-10 items-center justify-center gap-2 rounded border border-line px-3 text-sm font-semibold text-slate-700 hover:bg-panel"
                aria-label={`${item.title}を新規タブで開く`}
              >
                <ExternalLink className="h-4 w-4" aria-hidden="true" />
                <span>ソース</span>
              </a>
            </div>
            <p className="mt-3 text-sm leading-6 text-slate-700">{item.summary}</p>
            <div className="mt-3 grid gap-2 text-xs text-slate-600 sm:grid-cols-2 lg:grid-cols-4">
              <p>為替: {item.market_impact.fx}</p>
              <p>債券: {item.market_impact.bonds}</p>
              <p>株式: {item.market_impact.stocks}</p>
              <p>商品: {item.market_impact.commodities}</p>
            </div>
            <div className="mt-3 flex flex-wrap gap-2">
              {item.tags.map((tag) => (
                <span key={tag} className="rounded bg-slate-100 px-2 py-1 text-xs text-slate-600">{tag}</span>
              ))}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
