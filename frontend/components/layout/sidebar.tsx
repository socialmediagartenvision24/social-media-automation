"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navigation = [
  { label: "Übersicht", href: "/dashboard" },
  { label: "Accounts", href: "/dashboard/accounts" },
  { label: "Videos", href: "/dashboard/videos" },
  { label: "Kampagnen", href: "/dashboard/campaigns" },
  { label: "Kalender", href: "/dashboard/calendar" },
  { label: "Queue", href: "/dashboard/queue" },
  { label: "Analytics", href: "/dashboard/analytics" },
  {
    label: "Benachrichtigungen",
    href: "/dashboard/notifications",
  },
  { label: "Logs", href: "/dashboard/logs" },
  { label: "Einstellungen", href: "/dashboard/settings" },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-zinc-800 bg-zinc-950 lg:block">
      <div className="border-b border-zinc-800 px-6 py-5">
        <Link href="/dashboard">
          <h1 className="text-lg font-semibold">
            Social Automation
          </h1>

          <p className="mt-1 text-xs text-zinc-500">
            Control Center
          </p>
        </Link>
      </div>

      <nav className="space-y-1 p-4">
        {navigation.map((item) => {
          const active =
            pathname === item.href ||
            (item.href !== "/dashboard" &&
              pathname.startsWith(item.href));

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`block rounded-lg px-4 py-3 text-sm transition ${
                active
                  ? "bg-zinc-800 text-white"
                  : "text-zinc-400 hover:bg-zinc-900 hover:text-white"
              }`}
            >
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
