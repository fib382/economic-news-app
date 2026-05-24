import { AlertTriangle, Clock3, Newspaper, RadioTower } from "lucide-react";
import { formatDateTime } from "../lib/format";
import type { DailyReportPayload, MarketSnapshotItem, NewsItem } from "../lib/types";
import { ImportanceBadge } from "./ImportanceBadge";

interface DashboardProps {
  news: NewsItem[];
  markets: MarketSnapshotItem[];
  report: DailyReportPayload;
  generatedAt: string;
}

export function Dashboard({ news, markets, report, generatedAt }: DashboardProps) {
  const important = news.filter((item) => item.importance === "A").slice(0, 4);
  const importantCount = news.filter((item) => item.importance === "A").length;
  const middleEast = news.filter((item) => item.category === "イラン・中東情勢").slice(0, 3);
  const frb = news.filter((item) => item.category === "FRB").slice(0, 3);
  const headlineMarkets = markets.slice(0, 6);

  return (
    <section id="dashboard" className="space-y-4">
      <div className="grid gap-3 lg:grid-cols-[1.4fr_0.8fr]">
        <div className="rounded-lg border border-line bg-white p-5 shadow-subtle">
          <div className="flex items-center gap-2 text-sm font-semibold text-signal">
            <RadioTower className="h-4 w-4" aria-hidden="true" />
            今日の総括
          </div>
          <h2 className="mt-2 text-2xl font-bold text-ink">{report.headline}</h2>
          <p className="mt-3 text-sm leading-6 text-slate-700">{report.executive_summary}</p>
        </div>
        <div className="grid gap-3 sm:grid-cols-3 lg:grid-cols-1">
          <div className="rounded-lg border border-line bg-white p-4 shadow-subtle">
            <p className="flex items-center gap-2 text-sm text-slate-600"><Newspaper className="h-4 w-4" aria-hidden="true" />ニュース</p>
            <p className="mt-2 text-2xl font-bold">{news.length}</p>
          </div>
          <div className="rounded-lg border border-risk bg-white p-4 shadow-subtle">
            <p className="flex items-center gap-2 text-sm text-slate-600"><AlertTriangle className="h-4 w-4" aria-hidden="true" />重要度A</p>
            <p className="mt-2 text-2xl font-bold text-risk">{importantCount}</p>
          </div>
          <div className="rounded-lg border border-line bg-white p-4 shadow-subtle">
            <p className="flex items-center gap-2 text-sm text-slate-600"><Clock3 className="h-4 w-4" aria-hidden="true" />最終更新</p>
            <p className="mt-2 text-sm font-semibold">{formatDateTime(generatedAt)}</p>
          </div>
        </div>
      </div>

      <div className="grid gap-4 xl:grid-cols-3">
        <Panel title="重要度Aニュース" items={important} />
        <Panel title="イラン・中東情勢" items={middleEast} />
        <Panel title="FRB動向" items={frb} />
      </div>

      <div className="rounded-lg border border-line bg-white p-4 shadow-subtle">
        <h3 className="text-sm font-semibold text-ink">主要市場スナップショット</h3>
        <div className="mt-3 grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
          {headlineMarkets.map((item) => (
            <div key={item.symbol} className="flex items-center justify-between rounded border border-line bg-panel px-3 py-2">
              <span className="text-sm font-medium">{item.name}</span>
              <span className="text-sm font-bold">{item.value === null ? "未取得" : `${item.value}${item.unit}`}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function Panel({ title, items }: { title: string; items: NewsItem[] }) {
  return (
    <div className="rounded-lg border border-line bg-white p-4 shadow-subtle">
      <h3 className="text-sm font-semibold text-ink">{title}</h3>
      <div className="mt-3 space-y-3">
        {items.length === 0 ? (
          <p className="text-sm text-slate-500">該当ニュースはありません。</p>
        ) : (
          items.map((item) => (
            <a key={item.id} href={item.url} target="_blank" rel="noreferrer" className="block rounded border border-line p-3 hover:bg-panel">
              <div className="flex items-center justify-between gap-2">
                <span className="text-xs text-slate-500">{item.source}</span>
                <ImportanceBadge value={item.importance} />
              </div>
              <p className="mt-2 text-sm font-semibold leading-5 text-ink">{item.title}</p>
            </a>
          ))
        )}
      </div>
    </div>
  );
}
