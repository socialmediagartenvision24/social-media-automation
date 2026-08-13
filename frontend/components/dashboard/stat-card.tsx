interface StatCardProps {
  label: string;
  value: string | number;
  description?: string;
}

export function StatCard({
  label,
  value,
  description,
}: StatCardProps) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
      <p className="text-sm text-zinc-500">{label}</p>

      <p className="mt-3 text-3xl font-semibold">
        {value}
      </p>

      {description && (
        <p className="mt-2 text-xs text-zinc-600">
          {description}
        </p>
      )}
    </div>
  );
}
