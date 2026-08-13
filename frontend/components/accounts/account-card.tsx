import { Badge } from "@/components/ui/badge";
import type { SocialAccount } from "@/types/account";

interface AccountCardProps {
  account: SocialAccount;
}

export function AccountCard({
  account,
}: AccountCardProps) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="font-medium">{account.name}</p>

          <p className="mt-1 text-xs text-zinc-500">
            {account.platform}
          </p>
        </div>

        <Badge
          variant={
            account.status === "connected"
              ? "success"
              : "danger"
          }
        >
          {account.status === "connected"
            ? "Verbunden"
            : "Nicht verbunden"}
        </Badge>
      </div>

      <div className="mt-5 border-t border-zinc-800 pt-4">
        <p className="text-xs text-zinc-500">
          Zeitzone
        </p>

        <p className="mt-1 text-sm text-zinc-300">
          {account.timezone}
        </p>
      </div>
    </div>
  );
}
