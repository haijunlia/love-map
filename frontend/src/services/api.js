async function request(url, options = {}) {
  const response = await fetch(url, {
    headers: {
      ...(options.body instanceof FormData ? {} : { "Content-Type": "application/json" }),
      ...(options.headers || {})
    },
    ...options
  });

  if (!response.ok) {
    let message = "请求失败";
    try {
      const payload = await response.json();
      message = payload.detail || message;
    } catch {
      // 非 JSON 错误响应使用默认提示。
    }
    throw new Error(message);
  }

  if (response.status === 204) {
    return null;
  }
  return response.json();
}

function upload(url, file) {
  const body = new FormData();
  body.append("file", file);
  return request(url, { method: "POST", body });
}

export const api = {
  getCouple: () => request("/api/couple"),
  saveCouple: (data) => request("/api/couple", { method: "POST", body: JSON.stringify(data) }),
  listDiaries: (filters = {}) => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value) params.set(key, value);
    });
    const query = params.toString();
    return request("/api/diary" + (query ? "?" + query : ""));
  },
  createDiary: (data) => request("/api/diary", { method: "POST", body: JSON.stringify(data) }),
  updateDiary: (id, data) =>
    request("/api/diary/" + id, { method: "PUT", body: JSON.stringify(data) }),
  deleteDiary: (id) => request("/api/diary/" + id, { method: "DELETE" }),
  uploadDiaryPhoto: (id, file) => upload("/api/diary/" + id + "/photo", file),
  listPlaces: () => request("/api/place"),
  createPlace: (data) => request("/api/place", { method: "POST", body: JSON.stringify(data) }),
  updatePlace: (id, data) =>
    request("/api/place/" + id, { method: "PUT", body: JSON.stringify(data) }),
  deletePlace: (id) => request("/api/place/" + id, { method: "DELETE" }),
  uploadPlacePhoto: (id, file) => upload("/api/place/" + id + "/photo", file),
  getStats: () => request("/api/stats")
};
