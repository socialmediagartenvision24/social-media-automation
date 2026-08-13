import { EmptyState } from "@/components/ui/empty-state";

interface UpcomingPost {
  id: string;
  accountName: string;
  platform: string;
  scheduledAt: string;
}

interface UpcomingPostsProps {
  posts: UpcomingPost[];
}

export function UpcomingPosts({
  posts,
}: UpcomingPostsProps) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
      <h3 className="font-semibold">
        Nächste Veröffentlichungen
      </h3>

      <div className="mt-5">
        {posts.length === 0 ? (
          <EmptyState
            title="Keine geplanten Posts"
            description="Sobald Kampagnen aktiv sind, erscheinen die nächsten Veröffentlichungen hier."
          />
        ) : (
          <div className="space-y-3">
            {posts.map((post) => (
              <div
                key={post.id}
                className="flex items-center justify-between rounded-lg border border-zinc-800 p-4"
              >
                <div>
                  <p className="text-sm font-medium">
                    {post.accountName}
                  </p>

                  <p className="mt-1 text-xs text-zinc-500">
                    {post.platform}
                  </p>
                </div>

                <p className="text-xs text-zinc-500">
                  {post.scheduledAt}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
