interface CalendarPost {
  id: string;
  date: string;
  time: string;
  accountName: string;
  platform: string;
  status: string;
}

interface ContentCalendarProps {
  posts: CalendarPost[];
}

export function ContentCalendar({
  posts,
}: ContentCalendarProps) {
  if (posts.length === 0) {
    return (
      <div className="grid min-h-[400px] place-items-center rounded-xl border border-dashed border-zinc-800">
        <p className="text-sm text-zinc-600">
          Keine geplanten Veröffentlichungen.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {posts.map((post) => (
        <div
          key={post.id}
          className="flex items-center justify-between rounded-lg border border-zinc-800 bg-zinc-900 p-4"
        >
          <div>
            <p className="text-sm font-medium">
              {post.accountName}
            </p>

            <p className="mt-1 text-xs text-zinc-500">
              {post.platform}
            </p>
          </div>

          <div className="text-right">
            <p className="text-sm">{post.date}</p>
            <p className="mt-1 text-xs text-zinc-500">
              {post.time}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}
