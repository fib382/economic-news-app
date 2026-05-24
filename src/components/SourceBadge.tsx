export function SourceBadge({ source }: { source: string }) {
  return (
    <span className="inline-flex items-center rounded border border-line bg-white px-2 py-1 text-xs font-medium text-slate-700">
      {source}
    </span>
  );
}
