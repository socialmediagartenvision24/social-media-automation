const statuses = [
  "Pending",
  "Processing",
  "Published",
  "Failed",
];

export default function QueuePage() {
  return (
    <div className="space-y-8">
      <header>
        <h2 className="text-3xl font-semibold tracking-tight">
          Publishing Queue
        </h2>

        <p className="mt-2 text-zinc-400">
          Überwache alle geplanten und laufenden Veröffentlichungsjobs.
        </p>
      </header>

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {statuses.map((status) => (
          <div
            key={status}
            className="rounded-xl border border-zinc-800 bg-zinc-900 p-5"
          >
            <p className="text-sm text-zinc-500">{status}</p>
            <p className="mt-3 text-2xl font-semibold">0</p>
          </div>
        ))}
      </section>

      <section className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
        <h3 className="font-semibold">Jobs</h3>

        <div className="mt-6 rounded-lg border border-dashed border-zinc-800 p-10 text-center">
          <p className="text-sm text-zinc-500">
            Die Queue enthält aktuell keine Jobs.
          </p>
        </div>
      </section>
    </div>
  );
}
