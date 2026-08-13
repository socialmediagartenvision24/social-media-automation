export default function SettingsPage() {
  return (
    <div className="space-y-8">
      <header>
        <h2 className="text-3xl font-semibold tracking-tight">
          Einstellungen
        </h2>

        <p className="mt-2 text-zinc-400">
          Globale Einstellungen für die Plattform.
        </p>
      </header>

      <section className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
        <h3 className="font-semibold">Allgemein</h3>

        <div className="mt-6 space-y-5">
          <div>
            <label className="mb-2 block text-sm text-zinc-400">
              Standard-Zeitzone
            </label>

            <select
              defaultValue="Europe/Berlin"
              className="w-full max-w-md rounded-lg border border-zinc-700 bg-zinc-950 px-4 py-3 text-sm text-white outline-none"
            >
              <option value="Europe/Berlin">Europe/Berlin</option>
              <option value="UTC">UTC</option>
              <option value="America/New_York">
                America/New_York
              </option>
              <option value="America/Los_Angeles">
                America/Los_Angeles
              </option>
            </select>
          </div>

          <div>
            <label className="mb-2 block text-sm text-zinc-400">
              Standard Retry-Anzahl
            </label>

            <input
              type="number"
              min="0"
              max="10"
              defaultValue="3"
              className="w-full max-w-md rounded-lg border border-zinc-700 bg-zinc-950 px-4 py-3 text-sm text-white outline-none"
            />
          </div>
        </div>
      </section>

      <section className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
        <h3 className="font-semibold">System</h3>

        <div className="mt-5 space-y-3 text-sm text-zinc-500">
          <p>Backend: Nicht verbunden</p>
          <p>Worker: Nicht verbunden</p>
          <p>Supabase: Nicht verbunden</p>
        </div>
      </section>
    </div>
  );
}
