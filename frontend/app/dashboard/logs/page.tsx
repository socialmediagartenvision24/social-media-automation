export default function LogsPage() {
  return (
    <div className="space-y-8">
      <header>
        <h2 className="text-3xl font-semibold tracking-tight">Logs</h2>

        <p className="mt-2 text-zinc-400">
          Technische Ereignisse und Veröffentlichungsprotokolle.
        </p>
      </header>

      <section className="rounded-xl border border-zinc-800 bg-zinc-900">
        <div className="border-b border-zinc-800 p-6">
          <h3 className="font-semibold">System Logs</h3>
        </div>

        <div className="p-10 text-center">
          <p className="text-sm text-zinc-500">
            Noch keine Logs vorhanden.
          </p>
        </div>
      </section>
    </div>
  );
}
