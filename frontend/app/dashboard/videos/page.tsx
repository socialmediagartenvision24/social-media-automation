export default function VideosPage() {
  return (
    <div className="space-y-8">
      <header className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <h2 className="text-3xl font-semibold tracking-tight">
            Video-Mediathek
          </h2>

          <p className="mt-2 text-zinc-400">
            Lade Videos hoch und verwalte deine Content-Bibliothek.
          </p>
        </div>

        <button className="rounded-lg bg-white px-4 py-2.5 text-sm font-semibold text-black hover:bg-zinc-200">
          Videos hochladen
        </button>
      </header>

      <section className="rounded-xl border border-zinc-800 bg-zinc-900 p-10 text-center">
        <div className="mx-auto max-w-md">
          <h3 className="font-semibold">Noch keine Videos</h3>

          <p className="mt-2 text-sm text-zinc-500">
            Lade deine ersten Videos hoch, um eine Kampagne zu erstellen.
          </p>

          <button className="mt-6 rounded-lg border border-zinc-700 px-5 py-2.5 text-sm text-zinc-300 hover:bg-zinc-800">
            Video auswählen
          </button>
        </div>
      </section>
    </div>
  );
}
