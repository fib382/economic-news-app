import { CheckCircle2 } from "lucide-react";
import { formatDateTime } from "../lib/format";
import type { DailyReportPayload } from "../lib/types";
import { ImportanceBadge } from "./ImportanceBadge";

export function DailyReport({ report }: { report: DailyReportPayload }) {
  return (
    <section id="report" className="space-y-4">
      <div>
        <h2 className="text-lg font-semibold text-ink">日次レポート</h2>
        <p className="text-sm text-slate-600">生成日時: {formatDateTime(report.generated_at)}</p>
      </div>
      <div className="rounded-lg border border-line bg-white p-5 shadow-subtle">
        <p className="text-xs font-semibold text-signal">{report.date}</p>
        <h3 className="mt-1 text-xl font-bold text-ink">{report.headline}</h3>
        <p className="mt-3 text-sm leading-6 text-slate-700">{report.executive_summary}</p>
      </div>
      <div className="grid gap-3 lg:grid-cols-2">
        {report.sections.map((section) => (
          <article key={section.title} className="rounded-lg border border-line bg-white p-4 shadow-subtle">
            <div className="flex items-center justify-between gap-3">
              <h3 className="font-semibold text-ink">{section.title}</h3>
              <ImportanceBadge value={section.importance} />
            </div>
            <p className="mt-3 text-sm leading-6 text-slate-700">{section.summary}</p>
          </article>
        ))}
      </div>
      <div className="rounded-lg border border-line bg-panel p-4">
        <h3 className="text-sm font-semibold text-ink">注目点</h3>
        <ul className="mt-3 grid gap-2 sm:grid-cols-2">
          {report.watch_points.map((point) => (
            <li key={point} className="flex gap-2 text-sm text-slate-700">
              <CheckCircle2 className="mt-0.5 h-4 w-4 flex-none text-signal" aria-hidden="true" />
              <span>{point}</span>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
