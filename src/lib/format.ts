import { format, parseISO } from "date-fns";

export function formatDateTime(value: string | null | undefined): string {
  if (!value) return "未取得";
  try {
    return format(parseISO(value), "yyyy/MM/dd HH:mm");
  } catch {
    return value;
  }
}

export function formatDate(value: string | null | undefined): string {
  if (!value) return "未取得";
  try {
    return format(parseISO(value), "yyyy/MM/dd");
  } catch {
    return value;
  }
}

export function formatNumber(value: number | null, unit = ""): string {
  if (value === null || Number.isNaN(value)) return "未取得";
  const digits = Math.abs(value) >= 100 ? 1 : 2;
  return `${value.toLocaleString("ja-JP", {
    maximumFractionDigits: digits,
    minimumFractionDigits: unit === "%" ? 2 : 0
  })}${unit}`;
}

export function formatChange(value: number | null, unit = ""): string {
  if (value === null || Number.isNaN(value)) return "前日比未取得";
  const sign = value > 0 ? "+" : "";
  return `${sign}${value.toFixed(unit === "%" ? 2 : 2)}${unit}`;
}
