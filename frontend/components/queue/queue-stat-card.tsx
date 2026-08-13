interface QueueStatCardProps {
  label: string;
  value: number;
}

export function QueueStatCard({
  label,
  value,
}: QueueStatCardProps) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
      <p className="text-sm text-zinc-500">{label}</p>

      <p className="mt-3 text-2xl font-semibold">
        {value}
      </p>
    </div>
  );
}
