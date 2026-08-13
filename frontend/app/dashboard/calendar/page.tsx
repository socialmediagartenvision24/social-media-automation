export default function CalendarPage() {
  return (
    <div className="space-y-8">
      <header>
        <h2 className="text-3xl font-semibold tracking-tight">Kalender</h2>

        <p className="mt-2 text-zinc-400">
          Übersicht über deine geplanten Veröffentlichungen.
        </p>
      </header>

      <section className="rounded-xl border border-zinc-800 bg-zinc-900">
        <div className="flex items-center justify-between border-b border-zinc-800 p-6">
          <div>
            <h3 className="font-semibold">Content-Kalender</h3>
            <p className="mt-1 text-sm text-zinc-500">
              Keine geplanten Posts.
            </p>
          </div>

          <button className="rounded-lg border border-zinc-700 px-4 py-2 text-sm text-zinc-300 hover:bg-zinc-800">
            Heute
          </button>
        </div>

        <div className="grid min-h-[400px] place-items-center p-10">
          <p className="text-sm text-zinc-600">
            Kalender wird mit geplanten Posts gefüllt.
          </p>
        </div>
      </section>
    </div>
  );
}
