import StatCard from "@/components/dashboard/StatCard";

import {
  Users,
  Building2,
  FileText,
  ShieldCheck,
} from "lucide-react";

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      {/* Header */}

      <div>
        <h1 className="text-3xl font-bold text-foreground">
          Dashboard
        </h1>

        <p className="mt-2 text-muted-foreground">
          Welcome to Enterprise AI Admin Panel
        </p>
      </div>

      {/* Stats */}

      <div className="grid gap-6 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard
          title="Total Users"
          value="2,540"
          change="+12%"
          icon={Users}
        />

        <StatCard
          title="Departments"
          value="18"
          change="+3%"
          icon={Building2}
        />

        <StatCard
          title="Documents"
          value="8,245"
          change="+22%"
          icon={FileText}
        />

        <StatCard
          title="Permissions"
          value="124"
          change="+8%"
          icon={ShieldCheck}
        />
      </div>
    </div>
  );
}