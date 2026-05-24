import { Database, FileText, LayoutDashboard, ListFilter, Settings } from "lucide-react";
import type { ReactNode } from "react";
import { useEffect, useMemo, useState } from "react";
import { Dashboard } from "./components/Dashboard";
import { DailyReport } from "./components/DailyReport";
import { MarketSnapshot } from "./components/MarketSnapshot";
import { NewsList } from "./components/NewsList";
import { formatDateTime } from "./lib/format";
import type { DailyReportPayload, MarketSnapshotPayload, NewsItemsPayload, SourcesPayload } from "./lib/types";

interface DataState {
  news: NewsItemsPayload | null;
  markets: MarketSnapshotPayload | null;
  report: DailyReportPayload | null;
  sources: SourcesPayload | null;
  error: string | null;
  loading: boolean;
}

const nav = [
  { href: "#dashboard", label: "ダッシュボード", icon: LayoutDashboard },
  { href: "#news", label: "ニュース", icon: ListFilter },
  { href: "#markets", label: "市場", icon: Database },
  { href: "#report", label: "レポート", icon: FileText },
  { href: "#sources", label: "ソース", icon: Settings }
];

async function loadJson<T>(path: string): Promise<T> {
  const response = await fetch(path, { cache: "no-cache" });
  if (!response.ok) throw new Error(`${path} の読み込みに失敗しました`);
  return response.json() as Promise<T>;
}

export default function App() {
  const [state, setState] = useState<DataState>({
    news: null,
    markets: null,
    report: null,
    sources: null,
    error: null,
    loading: true
  });

  useEffect(() => {
    Promise.all([
      loadJson<NewsItemsPayload>("data/news_items.json"),
      loadJson<MarketSnapshotPayload>("data/market_snapshot.json"),
      loadJson<DailyReportPayload>("data/daily_report.json"),
      loadJson<SourcesPayload>("data/sources.json")
    ])
      .then(([news, markets, report, sources]) => {
        setState({ news, markets, report, sources, error: null, loading: false });
      })
      .catch((error: unknown) => {
        setState((current) => ({
          ...current,
          error: error instanceof Error ? error.message : "データの読み込みに失敗しました",
          loading: false
        }));
      });
  }, []);

  const generatedAt = useMemo(() => {
    return state.news?.generated_at ?? state.markets?.generated_at ?? state.report?.generated_at ?? "";
  }, [state.news, state.markets, state.report]);

  if (state.loading) {
    return <Shell><div className="rounded-lg border border-line bg-white p-6">データを読み込み中です。</div></Shell>;
  }

  if (state.error || !state.news || !state.markets || !state.report || !state.sources) {
    return <Shell><div className="rounded-lg border border-risk bg-red-50 p-6 text-risk">{state.error ?? "必要なJSONが不足しています。"}</div></Shell>;
  }

  return (
    <Shell generatedAt={generatedAt}>
      <Dashboard news={state.news.items} markets={state.markets.items} report={state.report} generatedAt={generatedAt} />
      <NewsList items={state.news.items} />
      <MarketSnapshot items={state.markets.items} />
      <DailyReport report={state.report} />
      <section id="sources" className="space-y-3">
        <div>
          <h2 className="text-lg font-semibold text-ink">ソース一覧</h2>
          <p className="text-sm text-slate-600">Secrets未設定の任意ソースはスキップされます。</p>
        </div>
        <div className="overflow-hidden rounded-lg border border-line bg-white shadow-subtle">
          <div className="grid min-w-[720px] grid-cols-[1.2fr_1fr_0.8fr_0.7fr_0.8fr] border-b border-line bg-panel px-4 py-3 text-xs font-semibold text-slate-600">
            <span>ソース</span><span>用途</span><span>取得</span><span>優先度</span><span>状態</span>
          </div>
          <div className="overflow-x-auto">
            {state.sources.items.map((source) => (
              <a
                key={source.name}
                href={source.url}
                target="_blank"
                rel="noreferrer"
                className="grid min-w-[720px] grid-cols-[1.2fr_1fr_0.8fr_0.7fr_0.8fr] border-b border-line px-4 py-3 text-sm last:border-b-0 hover:bg-panel"
              >
                <span className="font-semibold text-ink">{source.name}</span>
                <span className="text-slate-600">{source.category}</span>
                <span className="text-slate-600">{source.method}</span>
                <span className="text-slate-600">{source.priority}</span>
                <span className="text-slate-600">{source.status}</span>
              </a>
            ))}
          </div>
        </div>
      </section>
    </Shell>
  );
}

function Shell({ children, generatedAt }: { children: ReactNode; generatedAt?: string }) {
  return (
    <div className="min-h-screen bg-[#eef1ed]">
      <header className="sticky top-0 z-10 border-b border-line bg-white/95 backdrop-blur">
        <div className="mx-auto flex max-w-7xl flex-col gap-3 px-4 py-3 sm:px-6 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <h1 className="text-xl font-bold text-ink">Macro Geopolitical Brief</h1>
            <p className="text-sm text-slate-600">無料公開情報によるマクロ・地政学ニュース整理</p>
          </div>
          <div className="flex items-center gap-2 overflow-x-auto no-scrollbar">
            {nav.map(({ href, label, icon: Icon }) => (
              <a key={href} href={href} className="inline-flex h-10 flex-none items-center gap-2 rounded border border-line px-3 text-sm font-semibold text-slate-700 hover:bg-panel">
                <Icon className="h-4 w-4" aria-hidden="true" />
                {label}
              </a>
            ))}
          </div>
        </div>
      </header>
      <main className="mx-auto max-w-7xl space-y-8 px-4 py-6 sm:px-6 lg:py-8">
        {generatedAt ? (
          <div className="rounded-lg border border-line bg-panel px-4 py-3 text-sm text-slate-700">
            最終更新: {formatDateTime(generatedAt)} / 投資助言ではなく公開情報の整理です。
          </div>
        ) : null}
        {children}
      </main>
    </div>
  );
}
