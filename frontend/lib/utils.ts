export function cn(
  ...classes: Array<
    string | false | null | undefined
  >
) {
  return classes
    .filter(Boolean)
    .join(" ");
}

/* -------------------------------------------------------------------------- */
/* Dates                                                                      */
/* -------------------------------------------------------------------------- */

export function formatDate(
  value: string | Date,
  locale = "de-DE",
) {
  const date =
    value instanceof Date
      ? value
      : new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "—";
  }

  return new Intl.DateTimeFormat(
    locale,
    {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    },
  ).format(date);
}

export function formatDateTime(
  value: string | Date,
  locale = "de-DE",
) {
  const date =
    value instanceof Date
      ? value
      : new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "—";
  }

  return new Intl.DateTimeFormat(
    locale,
    {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    },
  ).format(date);
}

/* -------------------------------------------------------------------------- */
/* Numbers                                                                    */
/* -------------------------------------------------------------------------- */

export function formatNumber(
  value: number,
  locale = "de-DE",
) {
  return new Intl.NumberFormat(
    locale,
  ).format(value);
}

export function formatPercentage(
  value: number,
  decimals = 1,
) {
  return `${value.toFixed(decimals)} %`;
}

/* -------------------------------------------------------------------------- */
/* File sizes                                                                 */
/* -------------------------------------------------------------------------- */

export function formatFileSize(
  bytes: number,
) {
  if (bytes <= 0) {
    return "0 B";
  }

  const units = [
    "B",
    "KB",
    "MB",
    "GB",
    "TB",
  ];

  const index = Math.floor(
    Math.log(bytes) / Math.log(1024),
  );

  const unitIndex = Math.min(
    index,
    units.length - 1,
  );

  const value =
    bytes /
    Math.pow(
      1024,
      unitIndex,
    );

  return `${value.toFixed(unitIndex === 0 ? 0 : 1)} ${units[unitIndex]}`;
}

/* -------------------------------------------------------------------------- */
/* Duration                                                                   */
/* -------------------------------------------------------------------------- */

export function formatDuration(
  seconds: number,
) {
  if (!Number.isFinite(seconds) || seconds < 0) {
    return "00:00";
  }

  const totalSeconds = Math.floor(
    seconds,
  );

  const hours = Math.floor(
    totalSeconds / 3600,
  );

  const minutes = Math.floor(
    (totalSeconds % 3600) / 60,
  );

  const remainingSeconds =
    totalSeconds % 60;

  if (hours > 0) {
    return [
      String(hours).padStart(2, "0"),
      String(minutes).padStart(2, "0"),
      String(remainingSeconds).padStart(
        2,
        "0",
      ),
    ].join(":");
  }

  return [
    String(minutes).padStart(2, "0"),
    String(remainingSeconds).padStart(
      2,
      "0",
    ),
  ].join(":");
}

/* -------------------------------------------------------------------------- */
/* Text                                                                       */
/* -------------------------------------------------------------------------- */

export function truncate(
  text: string,
  maxLength: number,
) {
  if (text.length <= maxLength) {
    return text;
  }

  return `${text.slice(
    0,
    Math.max(0, maxLength - 3),
  )}...`;
}

/* -------------------------------------------------------------------------- */
/* Platform                                                                   */
/* -------------------------------------------------------------------------- */

export function getPlatformLabel(
  platform: string,
) {
  const labels: Record<
    string,
    string
  > = {
    instagram: "Instagram",
    facebook: "Facebook",
    tiktok: "TikTok",
  };

  return (
    labels[platform.toLowerCase()] ??
    platform
  );
}

/* -------------------------------------------------------------------------- */
/* Status                                                                     */
/* -------------------------------------------------------------------------- */

export function getStatusLabel(
  status: string,
) {
  const labels: Record<
    string,
    string
  > = {
    pending: "Ausstehend",
    processing: "Wird verarbeitet",
    published: "Veröffentlicht",
    failed: "Fehlgeschlagen",
    active: "Aktiv",
    paused: "Pausiert",
    completed: "Abgeschlossen",
    ready: "Bereit",
    uploading: "Upload läuft",
  };

  return (
    labels[status.toLowerCase()] ??
    status
  );
}
