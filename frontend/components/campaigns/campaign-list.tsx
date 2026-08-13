import type { Campaign } from "@/types/campaign";
import { CampaignCard } from "./campaign-card";
import { EmptyState } from "@/components/ui/empty-state";

interface CampaignListProps {
  campaigns: Campaign[];
}

export function CampaignList({
  campaigns,
}: CampaignListProps) {
  if (campaigns.length === 0) {
    return (
      <EmptyState
        title="Keine Kampagnen"
        description="Erstelle eine Kampagne, um deine Videos automatisch zu veröffentlichen."
      />
    );
  }

  return (
    <div className="grid gap-4 lg:grid-cols-2">
      {campaigns.map((campaign) => (
        <CampaignCard
          key={campaign.id}
          campaign={campaign}
        />
      ))}
    </div>
  );
}
