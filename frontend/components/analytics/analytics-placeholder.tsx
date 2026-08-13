interface AnalyticsPlaceholderProps {
  title?: string;
}

export function AnalyticsPlaceholder({
  title = "Performance",
}: AnalyticsPlaceholderProps) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
      <h3 className="font-semibold">{title}</h3>

      <div className="mt-6 grid min-h-[300px] place-items-center rounded-lg border border-dashed border-zinc-800">
        <p className="text-sm text-zinc-600">
          Analytics-Daten werden angezeigt, sobald Daten vorhanden sind.
        </p>
      </div>
    </div>
  );
}
