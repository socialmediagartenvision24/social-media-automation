interface AnalyticsStatCardProps {
  label: string;
  value: string | number;
  change?: string;
}

export function AnalyticsStatCard({
  label,
  value,
  change,
}: AnalyticsStatCardProps) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
      <p className="text-sm text-zinc-500">{label}</p>

      <p className="mt-3 text-2xl font-semibold">
        {value}
      </p>

      {change && (
        <p className="mt-2 text-xs text-zinc-500">
          {change}
        </p>
      )}
    </div>
  );
}
