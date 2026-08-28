"use client";

import { useEffect, useState } from "react";

import DashboardHeader from "@/components/dashboard/DashboardHeader";
import StatCard from "@/components/dashboard/StatCard";
import RecentActivity from "@/components/dashboard/RecentActivity";
import DocumentTrendChart from "@/components/dashboard/DocumentTrendChart";
import RecentDocuments from "@/components/dashboard/RecentDocuments";
import AnimatedContainer from "@/components/common/AnimatedContainer";

import { getDashboard } from "@/lib/api/api";

import {
  Users,
  Building2,
  FileText,
} from "lucide-react";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export default function DashboardPage() {
  const [dashboard, setDashboard] = useState({
    total_users: 0,
    total_documents: 0,
    total_departments: 0,
  });

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const data = await getDashboard();
        setDashboard(data);
      } catch (error) {
        console.error("Failed to load dashboard:", error);
      }
    };

    loadDashboard();
  }, []);

  return (
    <AnimatedContainer>
      <div className="space-y-8">

        {/* Dashboard Header */}
        <DashboardHeader />

        {/* KPI Cards */}
        <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">

          <StatCard
            title="Total Users"
            value={dashboard.total_users.toString()}
            change="+12%"
            icon={Users}
          />

          <StatCard
            title="Documents"
            value={dashboard.total_documents.toString()}
            change="+22%"
            icon={FileText}
          />

          <StatCard
            title="Departments"
            value={dashboard.total_departments.toString()}
            change="+3%"
            icon={Building2}
          />

        </div>

        {/* Full Width Document Upload Trend */}
        {/* <Card className="rounded-2xl border-0 shadow-sm">
          <CardHeader>
            <CardTitle>Document Upload Trend</CardTitle>
          </CardHeader>

          <CardContent>
            <DocumentTrendChart />
          </CardContent>
        </Card> */}

        {/* Recent Activity */}
        <RecentActivity />

        {/* Recent Documents */}
        <RecentDocuments />

      </div>
    </AnimatedContainer>
  );
}