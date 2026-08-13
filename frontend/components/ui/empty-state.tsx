import type { ReactNode } from "react";

interface EmptyStateProps {
  title: string;
  description?: string;
  action?: ReactNode;
}

export function EmptyState({
  title,
  description,
  action,
}: EmptyStateProps) {
  return (
    <div className="rounded-xl border border-dashed border-zinc-800 p-10 text-center">
      <h3 className="font-semibold text-white">{title}</h3>

      {description && (
        <p className="mx-auto mt-2 max-w-md text-sm text-zinc-500">
          {description}
        </p>
      )}

      {action && <div className="mt-6">{action}</div>}
    </div>
  );
}
