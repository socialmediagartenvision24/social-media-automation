export default function NotificationsPage() {
  return (
    <div className="space-y-8">
      <header>
        <h2 className="text-3xl font-semibold tracking-tight">
          Benachrichtigungen
        </h2>

        <p className="mt-2 text-zinc-400">
          Wichtige Meldungen zu Accounts, Kampagnen und Veröffentlichungen.
        </p>
      </header>

      <section className="rounded-xl border border-zinc-800 bg-zinc-900 p-10 text-center">
        <h3 className="font-semibold">Alles sauber</h3>

        <p className="mt-2 text-sm text-zinc-500">
          Es gibt aktuell keine Benachrichtigungen.
        </p>
      </section>
    </div>
  );
}
