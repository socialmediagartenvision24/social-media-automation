import type { HTMLAttributes } from "react";

type BadgeVariant =
  | "default"
  | "success"
  | "warning"
  | "danger";

interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  variant?: BadgeVariant;
}

const variants: Record<BadgeVariant, string> = {
  default:
    "border-zinc-700 bg-zinc-800 text-zinc-300",
  success:
    "border-green-900/50 bg-green-950/40 text-green-400",
  warning:
    "border-yellow-900/50 bg-yellow-950/40 text-yellow-400",
  danger:
    "border-red-900/50 bg-red-950/40 text-red-400",
};

export function Badge({
  variant = "default",
  className = "",
  children,
  ...props
}: BadgeProps) {
  return (
    <span
      className={`inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-medium ${variants[variant]} ${className}`}
      {...props}
    >
      {children}
    </span>
  );
}
