export default function AccountsPage() {
  return (
    <div className="space-y-8">
      <header className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <h2 className="text-3xl font-semibold tracking-tight">Accounts</h2>

          <p className="mt-2 text-zinc-400">
            Verwalte deine Instagram-, Facebook- und TikTok-Accounts.
          </p>
        </div>

        <button className="rounded-lg bg-white px-4 py-2.5 text-sm font-semibold text-black hover:bg-zinc-200">
          Account verbinden
        </button>
      </header>

      <section className="rounded-xl border border-zinc-800 bg-zinc-900">
        <div className="border-b border-zinc-800 p-6">
          <h3 className="font-semibold">Verbundene Accounts</h3>
        </div>

        <div className="p-10 text-center">
          <p className="text-sm text-zinc-500">
            Noch keine Social-Media-Accounts verbunden.
          </p>

          <button className="mt-4 rounded-lg border border-zinc-700 px-4 py-2 text-sm text-zinc-300 hover:bg-zinc-800">
            Ersten Account verbinden
          </button>
        </div>
      </section>
    </div>
  );
}
