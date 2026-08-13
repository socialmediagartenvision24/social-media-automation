import { Badge } from "@/components/ui/badge";

interface QueueJob {
  id: string;
  accountName: string;
  platform: string;
  status: "pending" | "processing" | "published" | "failed";
  scheduledAt: string;
}

interface QueueTableProps {
  jobs: QueueJob[];
}

export function QueueTable({
  jobs,
}: QueueTableProps) {
  if (jobs.length === 0) {
    return (
      <div className="rounded-xl border border-dashed border-zinc-800 p-10 text-center">
        <p className="text-sm text-zinc-500">
          Keine Publishing-Jobs vorhanden.
        </p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto rounded-xl border border-zinc-800">
      <table className="w-full min-w-[700px] text-left text-sm">
        <thead className="border-b border-zinc-800 bg-zinc-900">
          <tr>
            <th className="px-5 py-4 font-medium text-zinc-400">
              Account
            </th>
            <th className="px-5 py-4 font-medium text-zinc-400">
              Plattform
            </th>
            <th className="px-5 py-4 font-medium text-zinc-400">
              Status
            </th>
            <th className="px-5 py-4 font-medium text-zinc-400">
              Geplant
            </th>
          </tr>
        </thead>

        <tbody>
          {jobs.map((job) => (
            <tr
              key={job.id}
              className="border-b border-zinc-800 last:border-0"
            >
              <td className="px-5 py-4">
                {job.accountName}
              </td>

              <td className="px-5 py-4 text-zinc-400">
                {job.platform}
              </td>

              <td className="px-5 py-4">
                <Badge
                  variant={
                    job.status === "published"
                      ? "success"
                      : job.status === "failed"
                        ? "danger"
                        : job.status === "processing"
                          ? "warning"
                          : "default"
                  }
                >
                  {job.status}
                </Badge>
              </td>

              <td className="px-5 py-4 text-zinc-500">
                {job.scheduledAt}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
