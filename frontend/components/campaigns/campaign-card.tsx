import type { Campaign } from "@/types/campaign";
import { Badge } from "@/components/ui/badge";

interface CampaignCardProps {
  campaign: Campaign;
}

export function CampaignCard({
  campaign,
}: CampaignCardProps) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h3 className="font-medium">
            {campaign.name}
          </h3>

          <p className="mt-1 text-sm text-zinc-500">
            {campaign.description || "Keine Beschreibung"}
          </p>
        </div>

        <Badge
          variant={
            campaign.status === "active"
              ? "success"
              : campaign.status === "paused"
                ? "warning"
                : "default"
          }
        >
          {campaign.status}
        </Badge>
      </div>

      <div className="mt-5 grid grid-cols-2 gap-4 border-t border-zinc-800 pt-4">
        <div>
          <p className="text-xs text-zinc-500">
            Videos
          </p>

          <p className="mt-1 text-lg font-semibold">
            {campaign.videoCount}
          </p>
        </div>

        <div>
          <p className="text-xs text-zinc-500">
            Accounts
          </p>

          <p className="mt-1 text-lg font-semibold">
            {campaign.accountCount}
          </p>
        </div>
      </div>

      <div className="mt-4 text-xs text-zinc-500">
        {campaign.postsPerDay} Posts / Tag
        {campaign.loopEnabled && " • Loop aktiviert"}
      </div>
    </div>
  );
}
