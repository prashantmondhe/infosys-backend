"use client";

import { useEffect, useState } from "react";

import DataTable from "@/components/common/DataTable";
import StatusBadge from "@/components/common/StatusBadge";

import { getActivityLogs } from "@/lib/api/api";

type Activity = {
  id: number;
  user_name: string;
  action: string;
  module: string;
  created_at: string;
};

export default function ActivityLogsTable() {
  const [logs, setLogs] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadActivities();
  }, []);

  const loadActivities = async () => {
    try {
      const data = await getActivityLogs();
      setLogs(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error("Failed to load activities:", error);
      setLogs([]);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="rounded-xl border p-6 text-center">
        Loading activities...
      </div>
    );
  }

  return (
    <DataTable
      columns={[
        {
          key: "user_name",
          label: "User",
        },
        {
          key: "action",
          label: "Action",
        },
        {
          key: "module",
          label: "Module",
        },
        {
          key: "created_at",
          label: "Timestamp",
          render: (value) =>
            new Date(value as string).toLocaleString(),
        },
        {
          key: "status",
          label: "Status",
          render: () => (
            <StatusBadge status="Active" />
          ),
        },
      ]}
      data={logs}
    />
  );
}