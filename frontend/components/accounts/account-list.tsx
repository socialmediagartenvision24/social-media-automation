import type { SocialAccount } from "@/types/account";
import { AccountCard } from "./account-card";
import { EmptyState } from "@/components/ui/empty-state";

interface AccountListProps {
  accounts: SocialAccount[];
}

export function AccountList({
  accounts,
}: AccountListProps) {
  if (accounts.length === 0) {
    return (
      <EmptyState
        title="Keine Accounts"
        description="Verbinde deinen ersten Instagram-, Facebook- oder TikTok-Account."
      />
    );
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
      {accounts.map((account) => (
        <AccountCard
          key={account.id}
          account={account}
        />
      ))}
    </div>
  );
}
