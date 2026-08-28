"use client";

import {
  Upload,
  UserPlus,
  Building2,
} from "lucide-react";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

type Props = {
  onUploadDocument: () => void;
  onCreateUser: () => void;
  onAddDepartment: () => void;
};

export default function QuickActions({
  onUploadDocument,
  onCreateUser,
  onAddDepartment,
}: Props) {
  const actions = [
    {
      title: "Upload Document",
      icon: Upload,
      action: onUploadDocument,
    },
    {
      title: "Create User",
      icon: UserPlus,
      action: onCreateUser,
    },
    {
      title: "Add Department",
      icon: Building2,
      action: onAddDepartment,
    },
  ];

  return (
    <Card className="rounded-2xl border-0 shadow-sm">
      <CardHeader>
        <CardTitle>Quick Actions</CardTitle>
      </CardHeader>

      <CardContent className="space-y-4">
        {actions.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.title}
              onClick={item.action}
              className="
                flex
                w-full
                items-center
                gap-4
                rounded-xl
                border
                border-slate-200
                bg-white
                p-4
                text-left
                transition-all
                duration-200
                hover:border-violet-500
                hover:bg-violet-50
                hover:shadow-md
              "
            >
              <div className="rounded-lg bg-violet-100 p-3">
                <Icon className="h-5 w-5 text-violet-600" />
              </div>

              <span className="font-medium">
                {item.title}
              </span>
            </button>
          );
        })}
      </CardContent>
    </Card>
  );
}