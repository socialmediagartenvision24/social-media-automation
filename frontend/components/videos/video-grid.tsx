import type { Video } from "@/types/video";
import { VideoCard } from "./video-card";
import { EmptyState } from "@/components/ui/empty-state";

interface VideoGridProps {
  videos: Video[];
}

export function VideoGrid({
  videos,
}: VideoGridProps) {
  if (videos.length === 0) {
    return (
      <EmptyState
        title="Keine Videos"
        description="Lade Videos hoch, um deine Content-Bibliothek aufzubauen."
      />
    );
  }

  return (
    <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      {videos.map((video) => (
        <VideoCard
          key={video.id}
          video={video}
        />
      ))}
    </div>
  );
}
