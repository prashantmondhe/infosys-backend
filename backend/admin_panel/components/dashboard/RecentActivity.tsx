"use client";

import { useEffect, useState } from "react";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

import { getActivityLogs } from "@/lib/api/api";

type Activity = {
  id: number;
  user_name: string;
  action: string;
  department_name: string;
  created_at: string;
};

export default function RecentActivity() {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadActivities();
  }, []);

  const loadActivities = async () => {
    try {
      const data = await getActivityLogs();

      console.log("Activity API Response:", data);

      setActivities(Array.isArray(data) ? data.slice(0, 5) : []);
    } catch (error) {
      console.error("Activity Error:", error);
      setActivities([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="rounded-2xl border border-border bg-card p-6 shadow-sm">
      <h2 className="mb-6 text-xl font-semibold">
        Recent Activity
      </h2>

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>User</TableHead>
            <TableHead>Action</TableHead>
            {/* <TableHead>Department</TableHead> */}
            <TableHead>Time</TableHead>
          </TableRow>
        </TableHeader>

        <TableBody>
          {loading ? (
            <TableRow>
              <TableCell colSpan={4} className="text-center py-6">
                Loading...
              </TableCell>
            </TableRow>
          ) : activities.length === 0 ? (
            <TableRow>
              <TableCell colSpan={4} className="text-center py-6">
                No activity found
              </TableCell>
            </TableRow>
          ) : (
            activities.map((item) => (
              <TableRow key={item.id}>
                <TableCell>{item.user_name}</TableCell>

                <TableCell>{item.action}</TableCell>

                {/* <TableCell>{item.department_name}</TableCell> */}

                <TableCell>
                  {new Date(item.created_at).toLocaleString()}
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </div>
  );
}