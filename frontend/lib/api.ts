const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface ApiOptions extends RequestInit {
  token?: string;
}

export class ApiError extends Error {
  status: number;
  data?: unknown;

  constructor(
    message: string,
    status: number,
    data?: unknown,
  ) {
    super(message);

    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
}

async function request<T>(
  endpoint: string,
  options: ApiOptions = {},
): Promise<T> {
  const {
    token,
    headers,
    ...fetchOptions
  } = options;

  const response = await fetch(
    `${API_URL}${endpoint}`,
    {
      ...fetchOptions,
      headers: {
        "Content-Type": "application/json",
        ...(token
          ? {
              Authorization: `Bearer ${token}`,
            }
          : {}),
        ...headers,
      },
    },
  );

  let data: unknown = null;

  const contentType =
    response.headers.get("content-type");

  if (contentType?.includes("application/json")) {
    data = await response.json();
  } else {
    data = await response.text();
  }

  if (!response.ok) {
    const message =
      typeof data === "object" &&
      data !== null &&
      "detail" in data &&
      typeof (data as { detail?: unknown }).detail ===
        "string"
        ? (data as { detail: string }).detail
        : `API request failed with status ${response.status}`;

    throw new ApiError(
      message,
      response.status,
      data,
    );
  }

  return data as T;
}

/* -------------------------------------------------------------------------- */
/* Health                                                                    */
/* -------------------------------------------------------------------------- */

export interface HealthResponse {
  status: string;
  version?: string;
}

export function getHealth() {
  return request<HealthResponse>("/health");
}

/* -------------------------------------------------------------------------- */
/* Accounts                                                                  */
/* -------------------------------------------------------------------------- */

export function getAccounts<T = unknown>(token?: string) {
  return request<T>("/accounts", {
    token,
  });
}

export function getAccount<T = unknown>(
  accountId: string,
  token?: string,
) {
  return request<T>(`/accounts/${accountId}`, {
    token,
  });
}

export function deleteAccount<T = unknown>(
  accountId: string,
  token?: string,
) {
  return request<T>(
    `/accounts/${accountId}`,
    {
      method: "DELETE",
      token,
    },
  );
}

/* -------------------------------------------------------------------------- */
/* Videos                                                                    */
/* -------------------------------------------------------------------------- */

export function getVideos<T = unknown>(token?: string) {
  return request<T>("/videos", {
    token,
  });
}

export function getVideo<T = unknown>(
  videoId: string,
  token?: string,
) {
  return request<T>(`/videos/${videoId}`, {
    token,
  });
}

export function deleteVideo<T = unknown>(
  videoId: string,
  token?: string,
) {
  return request<T>(
    `/videos/${videoId}`,
    {
      method: "DELETE",
      token,
    },
  );
}

/* -------------------------------------------------------------------------- */
/* Campaigns                                                                 */
/* -------------------------------------------------------------------------- */

export function getCampaigns<T = unknown>(
  token?: string,
) {
  return request<T>("/campaigns", {
    token,
  });
}

export function getCampaign<T = unknown>(
  campaignId: string,
  token?: string,
) {
  return request<T>(
    `/campaigns/${campaignId}`,
    {
      token,
    },
  );
}

export function createCampaign<
  T = unknown,
>(
  payload: unknown,
  token?: string,
) {
  return request<T>("/campaigns", {
    method: "POST",
    body: JSON.stringify(payload),
    token,
  });
}

export function updateCampaign<
  T = unknown,
>(
  campaignId: string,
  payload: unknown,
  token?: string,
) {
  return request<T>(
    `/campaigns/${campaignId}`,
    {
      method: "PATCH",
      body: JSON.stringify(payload),
      token,
    },
  );
}

export function deleteCampaign<
  T = unknown,
>(
  campaignId: string,
  token?: string,
) {
  return request<T>(
    `/campaigns/${campaignId}`,
    {
      method: "DELETE",
      token,
    },
  );
}

/* -------------------------------------------------------------------------- */
/* Posts / Queue                                                             */
/* -------------------------------------------------------------------------- */

export function getPosts<T = unknown>(
  params?: {
    status?: string;
    accountId?: string;
    campaignId?: string;
    limit?: number;
  },
  token?: string,
) {
  const searchParams =
    new URLSearchParams();

  if (params?.status) {
    searchParams.set(
      "status",
      params.status,
    );
  }

  if (params?.accountId) {
    searchParams.set(
      "account_id",
      params.accountId,
    );
  }

  if (params?.campaignId) {
    searchParams.set(
      "campaign_id",
      params.campaignId,
    );
  }

  if (params?.limit) {
    searchParams.set(
      "limit",
      String(params.limit),
    );
  }

  const query =
    searchParams.toString();

  return request<T>(
    `/posts${query ? `?${query}` : ""}`,
    {
      token,
    },
  );
}

export function getQueue<T = unknown>(
  token?: string,
) {
  return request<T>("/queue", {
    token,
  });
}

/* -------------------------------------------------------------------------- */
/* Analytics                                                                 */
/* -------------------------------------------------------------------------- */

export function getAnalytics<T = unknown>(
  params?: {
    from?: string;
    to?: string;
    accountId?: string;
    platform?: string;
  },
  token?: string,
) {
  const searchParams =
    new URLSearchParams();

  if (params?.from) {
    searchParams.set(
      "from",
      params.from,
    );
  }

  if (params?.to) {
    searchParams.set(
      "to",
      params.to,
    );
  }

  if (params?.accountId) {
    searchParams.set(
      "account_id",
      params.accountId,
    );
  }

  if (params?.platform) {
    searchParams.set(
      "platform",
      params.platform,
    );
  }

  const query =
    searchParams.toString();

  return request<T>(
    `/analytics${query ? `?${query}` : ""}`,
    {
      token,
    },
  );
}

/* -------------------------------------------------------------------------- */
/* Export                                                                     */
/* -------------------------------------------------------------------------- */

export const api = {
  getHealth,

  getAccounts,
  getAccount,
  deleteAccount,

  getVideos,
  getVideo,
  deleteVideo,

  getCampaigns,
  getCampaign,
  createCampaign,
  updateCampaign,
  deleteCampaign,

  getPosts,
  getQueue,

  getAnalytics,
};
