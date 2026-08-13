import Link from "next/link";

const navigation = [
  { label: "Übersicht", href: "/dashboard" },
  { label: "Accounts", href: "/dashboard/accounts" },
  { label: "Videos", href: "/dashboard/videos" },
  { label: "Kampagnen", href: "/dashboard/campaigns" },
  { label: "Kalender", href: "/dashboard/calendar" },
  { label: "Queue", href: "/dashboard/queue" },
  { label: "Analytics", href: "/dashboard/analytics" },
  { label: "Benachrichtigungen", href: "/dashboard/notifications" },
  { label: "Logs", href: "/dashboard/logs" },
  { label: "Einstellungen", href: "/dashboard/settings" },
];

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-zinc-950 text-white">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-zinc-800 bg-zinc-950 lg:block">
        <div className="border-b border-zinc-800 px-6 py-5">
          <Link href="/dashboard">
            <h1 className="text-lg font-semibold">Social Automation</h1>
            <p className="mt-1 text-xs text-zinc-500">Control Center</p>
          </Link>
        </div>

        <nav className="space-y-1 p-4">
          {navigation.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="block rounded-lg px-4 py-3 text-sm text-zinc-400 transition hover:bg-zinc-900 hover:text-white"
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>

      <main className="min-h-screen lg:pl-64">
        <div className="mx-auto max-w-7xl p-6 lg:p-8">{children}</div>
      </main>
    </div>
  );
}
