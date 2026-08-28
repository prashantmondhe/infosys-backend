const API_URL = "http://127.0.0.1:8000";

// =====================================================
// USERS APIs
// =====================================================

export async function getUsers() {
  const res = await fetch(`${API_URL}/users/`);

  if (!res.ok) {
    throw new Error("Failed to fetch users");
  }

  return await res.json();
}

export async function createUser(data: {
  name: string;
  email: string;
  role: string;
  department: string;
}) {
  const res = await fetch(`${API_URL}/users/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || "Failed to create user");
  }

  return await res.json();
}

export async function deleteUser(id: number) {
  const res = await fetch(`${API_URL}/users/${id}`, {
    method: "DELETE",
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || "Failed to delete user");
  }

  return await res.json();
}

// =====================================================
// DOCUMENT APIs
// =====================================================

export async function getDocuments() {
  const res = await fetch(`${API_URL}/documents/`);

  if (!res.ok) {
    throw new Error("Failed to fetch documents");
  }

  return await res.json();
}

export async function createDocument(data: FormData) {
  const res = await fetch(`${API_URL}/documents/`, {
    method: "POST",
    body: data,
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || "Failed to upload document");
  }

  return await res.json();
}

export async function deleteDocument(id: number) {
  const res = await fetch(`${API_URL}/documents/${id}`, {
    method: "DELETE",
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || "Failed to delete document");
  }

  return await res.json();
}

// =====================================================
// DEPARTMENTS APIs
// =====================================================

export async function getDepartments() {
  const res = await fetch(`${API_URL}/departments/`);

  if (!res.ok) {
    throw new Error("Failed to fetch departments");
  }

  return await res.json();
}

export async function createDepartment(data: {
  name: string;
  department_head: string;
  is_active: boolean;
}) {
  const res = await fetch(`${API_URL}/departments/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || "Failed to create department");
  }

  return await res.json();
}

export async function deleteDepartment(id: number) {
  const res = await fetch(`${API_URL}/departments/${id}`, {
    method: "DELETE",
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || "Failed to delete department");
  }

  return await res.json();
}

// =====================================================
// DASHBOARD APIs
// =====================================================

export async function getDashboard() {
  const res = await fetch(`${API_URL}/dashboard/`);

  if (!res.ok) {
    throw new Error("Failed to fetch dashboard");
  }

  return await res.json();
}

// =====================================================
// ACTIVITY LOG APIs
// =====================================================

export async function getActivityLogs() {
  const res = await fetch(`${API_URL}/activities/`);

  if (!res.ok) {
    throw new Error("Failed to fetch activity logs");
  }

  return await res.json();
}

export async function getDocumentTrend() {
  const res = await fetch(`${API_URL}/dashboard/document-trend`);

  if (!res.ok) {
    throw new Error("Failed to fetch document trend");
  }

  return await res.json();
}