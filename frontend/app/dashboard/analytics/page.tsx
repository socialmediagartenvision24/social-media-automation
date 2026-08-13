const stats = [
  "Veröffentlichungen",
  "Erfolgreich",
  "Fehlgeschlagen",
  "Erfolgsquote",
];

export default function AnalyticsPage() {
  return (
    <div className="space-y-8">
      <header>
        <h2 className="text-3xl font-semibold tracking-tight">
          Analytics
        </h2>

        <p className="mt-2 text-zinc-400">
          Übersicht über deine Veröffentlichungsdaten.
        </p>
      </header>

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {stats.map((stat) => (
          <div
            key={stat}
            className="rounded-xl border border-zinc-800 bg-zinc-900 p-5"
          >
            <p className="text-sm text-zinc-500">{stat}</p>
            <p className="mt-3 text-2xl font-semibold">0</p>
          </div>
        ))}
      </section>

      <section className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
        <h3 className="font-semibold">Performance</h3>

        <div className="mt-6 grid min-h-[300px] place-items-center rounded-lg border border-dashed border-zinc-800">
          <p className="text-sm text-zinc-600">
            Analytics-Daten werden angezeigt, sobald Veröffentlichungen
            vorhanden sind.
          </p>
        </div>
      </section>
    </div>
  );
}
