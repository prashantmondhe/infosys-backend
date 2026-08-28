"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

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
  Sparkles,
} from "lucide-react";

const menuItems = [
  {
    title: "Dashboard",
    href: "/admin/dashboard",
    icon: LayoutDashboard,
  },
  {
    title: "Documents",
    href: "/admin/documents",
    icon: FileText,
  },
  {
    title: "Users",
    href: "/admin/users",
    icon: Users,
  },
  {
    title: "Departments",
    href: "/admin/departments",
    icon: Building2,
  },
  // {
  //   title: "Permissions",
  //   href: "/admin/permissions",
  //   icon: ShieldCheck,
  // },
  {
    title: "Activity Logs",
    href: "/admin/activity-logs",
    icon: History,
  },
  // {
  //   title: "Storage",
  //   href: "/admin/storage",
  //   icon: HardDrive,
  // },
  // {
  //   title: "Reports",
  //   href: "/admin/reports",
  //   icon: FileBarChart2,
  // },
  // {
  //   title: "Settings",
  //   href: "/admin/settings",
  //   icon: Settings,
  // },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="flex h-screen w-72 flex-col border-r border-sidebar-border bg-sidebar text-sidebar-foreground">
      {/* Logo */}

      <div className="border-b border-sidebar-border px-7 py-8">
        <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-violet-600 to-indigo-600 shadow-lg shadow-violet-600/30">
          <Sparkles className="h-6 w-6 text-white" />
        </div>

        <h1 className="text-xl font-bold tracking-tight">
          Infosys AI Assistant
        </h1>

        <p className="mt-1 text-sm text-sidebar-foreground/70">
          Admin Dashboard
        </p>
      </div>

      {/* Menu */}   

      <nav className="flex-1 space-y-2 px-4 py-6">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const active = pathname === item.href;

          return (
            <Link
              key={item.title}
              href={item.href}
              className={`
                group
                flex
                items-center
                gap-3
                rounded-2xl
                px-4
                py-3
                text-sm
                font-medium
                transition-all
                duration-300

                ${
                  active
                    ? "bg-sidebar-primary text-sidebar-primary-foreground shadow-lg"
                    : "text-sidebar-foreground/70 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
                }
              `}
            >
              <Icon
                className={`h-5 w-5 transition-transform duration-300 ${
                  active ? "" : "group-hover:scale-110"
                }`}
              />

              <span>{item.title}</span>
            </Link>
          );
        })}
      </nav>

      {/* Profile */}

      <div className="border-t border-sidebar-border p-5">
        <div className="rounded-2xl border border-sidebar-border bg-sidebar-accent p-4">
          <div className="flex items-center gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-gradient-to-br from-violet-500 to-indigo-600 text-sm font-bold text-white shadow-md">
              RB
            </div>

            <div>
              <p className="text-sm font-semibold">
                Rohan Bhesara
              </p>

              <p className="text-xs text-sidebar-foreground/70">
                Super Admin
              </p>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
}