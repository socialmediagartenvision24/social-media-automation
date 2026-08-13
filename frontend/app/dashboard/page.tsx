const stats = [
  {
    label: "Aktive Accounts",
    value: "0",
  },
  {
    label: "Aktive Kampagnen",
    value: "0",
  },
  {
    label: "Posts heute",
    value: "0",
  },
  {
    label: "Fehlgeschlagen",
    value: "0",
  },
];

const services = [
  "Backend",
  "Worker",
  "Database",
  "Storage",
  "Instagram",
  "Facebook",
  "TikTok",
];

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      <header>
        <h2 className="text-3xl font-semibold tracking-tight">
          Übersicht
        </h2>

        <p className="mt-2 text-zinc-400">
          Zentrale Übersicht deiner Social-Media-Automatisierung.
        </p>
      </header>

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {stats.map((stat) => (
          <div
            key={stat.label}
            className="rounded-xl border border-zinc-800 bg-zinc-900 p-5"
          >
            <p className="text-sm text-zinc-500">{stat.label}</p>
            <p className="mt-3 text-3xl font-semibold">{stat.value}</p>
          </div>
        ))}
      </section>

      <section className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
          <h3 className="font-semibold">Nächste Veröffentlichungen</h3>

          <div className="mt-6 rounded-lg border border-dashed border-zinc-800 p-8 text-center">
            <p className="text-sm text-zinc-500">
              Noch keine geplanten Veröffentlichungen.
            </p>
          </div>
        </div>

        <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
          <h3 className="font-semibold">Systemstatus</h3>

          <div className="mt-5 space-y-3">
            {services.map((service) => (
              <div
                key={service}
                className="flex items-center justify-between border-b border-zinc-800 pb-3 last:border-0"
              >
                <span className="text-sm text-zinc-300">{service}</span>

                <span className="text-xs text-zinc-600">
                  Nicht verbunden
                </span>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
