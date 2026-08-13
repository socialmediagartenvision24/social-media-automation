import type { Video } from "@/types/video";
import { Badge } from "@/components/ui/badge";

interface VideoCardProps {
  video: Video;
}

export function VideoCard({
  video,
}: VideoCardProps) {
  return (
    <div className="overflow-hidden rounded-xl border border-zinc-800 bg-zinc-900">
      <div className="aspect-video bg-zinc-950">
        {video.thumbnailUrl ? (
          <img
            src={video.thumbnailUrl}
            alt={video.name}
            className="h-full w-full object-cover"
          />
        ) : (
          <div className="grid h-full place-items-center text-xs text-zinc-600">
            Keine Vorschau
          </div>
        )}
      </div>

      <div className="p-4">
        <div className="flex items-start justify-between gap-3">
          <h3 className="truncate text-sm font-medium">
            {video.name}
          </h3>

          <Badge
            variant={
              video.status === "ready"
                ? "success"
                : video.status === "failed"
                  ? "danger"
                  : "warning"
            }
          >
            {video.status}
          </Badge>
        </div>

        <div className="mt-3 flex justify-between text-xs text-zinc-500">
          <span>{video.durationSeconds}s</span>
          <span>{video.fileSizeMb} MB</span>
        </div>
      </div>
    </div>
  );
}
