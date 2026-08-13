export type VideoStatus =
  | "uploading"
  | "processing"
  | "ready"
  | "failed"
  | "deleted";

export interface Video {
  id: string;

  name: string;

  description?: string | null;

  storagePath: string;

  publicUrl?: string | null;

  thumbnailUrl?: string | null;

  mimeType: string;

  fileSizeBytes: number;

  fileSizeMb: number;

  durationSeconds: number;

  width?: number | null;

  height?: number | null;

  status: VideoStatus;

  createdAt: string;

  updatedAt: string;
}

export interface CreateVideoInput {
  name: string;

  description?: string;

  storagePath: string;

  mimeType: string;

  fileSizeBytes: number;
}

export interface VideoUploadProgress {
  videoId: string;

  progress: number;

  status: VideoStatus;

  error?: string | null;
}
