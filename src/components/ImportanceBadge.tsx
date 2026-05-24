import type { Importance } from "../lib/types";

const styles: Record<Importance, string> = {
  A: "border-risk bg-red-50 text-risk",
  B: "border-amberline bg-amber-50 text-amber-800",
  C: "border-slate-300 bg-slate-50 text-slate-600"
};

export function ImportanceBadge({ value }: { value: Importance }) {
  return (
    <span className={`inline-flex h-7 min-w-7 items-center justify-center rounded border px-2 text-xs font-bold ${styles[value]}`}>
      {value}
    </span>
  );
}
