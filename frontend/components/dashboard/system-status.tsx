import { Badge } from "@/components/ui/badge";

interface SystemService {
  name: string;
  status: "online" | "offline" | "warning";
}

interface SystemStatusProps {
  services: SystemService[];
}

export function SystemStatus({
  services,
}: SystemStatusProps) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
      <h3 className="font-semibold">Systemstatus</h3>

      <div className="mt-5 space-y-3">
        {services.map((service) => {
          const variant =
            service.status === "online"
              ? "success"
              : service.status === "warning"
                ? "warning"
                : "danger";

          return (
            <div
              key={service.name}
              className="flex items-center justify-between border-b border-zinc-800 pb-3 last:border-0"
            >
              <span className="text-sm text-zinc-300">
                {service.name}
              </span>

              <Badge variant={variant}>
                {service.status === "online"
                  ? "Online"
                  : service.status === "warning"
                    ? "Warnung"
                    : "Offline"}
              </Badge>
            </div>
          );
        })}
      </div>
    </div>
  );
}
