import { ArrowDownRight, ArrowUpRight, Minus } from "lucide-react";
import { formatChange, formatDate, formatNumber } from "../lib/format";
import type { MarketSnapshotItem } from "../lib/types";

function ChangeIcon({ value }: { value: number | null }) {
  if (value === null || value === 0) return <Minus className="h-4 w-4" aria-hidden="true" />;
  if (value > 0) return <ArrowUpRight className="h-4 w-4" aria-hidden="true" />;
  return <ArrowDownRight className="h-4 w-4" aria-hidden="true" />;
}

export function MarketSnapshot({ items }: { items: MarketSnapshotItem[] }) {
  return (
    <section id="markets" className="space-y-3">
      <div>
        <h2 className="text-lg font-semibold text-ink">市場データ</h2>
        <p className="text-sm text-slate-600">取得できない系列は未取得として表示します。</p>
      </div>
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-4">
        {items.map((item) => (
          <article key={item.symbol} className="rounded-lg border border-line bg-white p-4 shadow-subtle">
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">{item.symbol}</p>
                <h3 className="mt-1 text-sm font-semibold text-ink">{item.name}</h3>
              </div>
              <span className="rounded border border-line px-2 py-1 text-xs text-slate-600">{item.category}</span>
            </div>
            <div className="mt-4 flex items-end justify-between gap-3">
              <p className="text-2xl font-bold text-ink">{formatNumber(item.value, item.unit)}</p>
              <p className={`flex items-center gap-1 text-sm font-semibold ${item.change_1d && item.change_1d > 0 ? "text-risk" : item.change_1d && item.change_1d < 0 ? "text-signal" : "text-slate-500"}`}>
                <ChangeIcon value={item.change_1d} />
                {formatChange(item.change_1d, item.unit)}
              </p>
            </div>
            <p className="mt-3 text-xs text-slate-500">{item.source} / {formatDate(item.date)}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
