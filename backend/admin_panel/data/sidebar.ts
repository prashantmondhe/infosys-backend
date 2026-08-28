import {
  LayoutDashboard,
  FileText,
  Users,
  Building2,
  ShieldCheck,
  History,
  HardDrive,
  FileBarChart2,
  Settings,
} from "lucide-react";

export const sidebarItems = [
  {
    title: "Dashboard",
    icon: LayoutDashboard,
    href: "/admin/dashboard",
  },
  {
    title: "Documents",
    icon: FileText,
    href: "/admin/documents",
  },
  {
    title: "Users",
    icon: Users,
    href: "/admin/users",
  },
  {
    title: "Departments",
    icon: Building2,
    href: "/admin/departments",
  },
  {
    title: "Permissions",
    icon: ShieldCheck,
    href: "/admin/permissions",
  },
  {
    title: "Activity Logs",
    icon: History,
    href: "/admin/activity-logs",
  },
  {
    title: "Storage",
    icon: HardDrive,
    href: "/admin/storage",
  },
  {
    title: "Reports",
    icon: FileBarChart2,
    href: "/admin/reports",
  },
  {
    title: "Settings",
    icon: Settings,
    href: "/admin/settings",
  },
];