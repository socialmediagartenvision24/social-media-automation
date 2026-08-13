export default function CampaignsPage() {
  return (
    <div className="space-y-8">
      <header className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <h2 className="text-3xl font-semibold tracking-tight">
            Kampagnen
          </h2>

          <p className="mt-2 text-zinc-400">
            Erstelle wiederkehrende Content-Kampagnen.
          </p>
        </div>

        <button className="rounded-lg bg-white px-4 py-2.5 text-sm font-semibold text-black hover:bg-zinc-200">
          Neue Kampagne
        </button>
      </header>

      <section className="rounded-xl border border-zinc-800 bg-zinc-900">
        <div className="border-b border-zinc-800 p-6">
          <h3 className="font-semibold">Deine Kampagnen</h3>
        </div>

        <div className="p-10 text-center">
          <p className="text-sm text-zinc-500">
            Noch keine Kampagnen erstellt.
          </p>

          <p className="mt-2 text-xs text-zinc-600">
            Kampagnen können später automatisch wiederholt werden.
          </p>
        </div>
      </section>
    </div>
  );
}
