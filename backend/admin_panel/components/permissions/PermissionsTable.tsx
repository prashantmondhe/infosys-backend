"use client";

import DataTable from "@/components/common/DataTable";
import { Button } from "@/components/ui/button";

import {
  Eye,
  Pencil,
  Trash2,
} from "lucide-react";

type Role = {
  id: number;
  role: string;
  users: number;
  permissions: number;
};

const roles: Role[] = [
  {
    id: 1,
    role: "Super Admin",
    users: 1,
    permissions: 32,
  },
  {
    id: 2,
    role: "Admin",
    users: 4,
    permissions: 28,
  },
  {
    id: 3,
    role: "Manager",
    users: 11,
    permissions: 20,
  },
  {
    id: 4,
    role: "Employee",
    users: 57,
    permissions: 8,
  },
];

export default function PermissionsTable() {
  return (
    <DataTable
      columns={[
        {
          key: "role",
          label: "Role",
        },
        {
          key: "users",
          label: "Assigned Users",
        },
        {
          key: "permissions",
          label: "Permissions",
          render: (value) => (
            <span className="font-medium">
              {String(value)} Access
            </span>
          ),
        },
        {
          key: "id",
          label: "Actions",
          render: () => (
            <div className="flex gap-2">
              <Button size="icon" variant="ghost">
                <Eye className="h-4 w-4" />
              </Button>

              <Button size="icon" variant="ghost">
                <Pencil className="h-4 w-4" />
              </Button>

              <Button size="icon" variant="ghost">
                <Trash2 className="h-4 w-4 text-red-500" />
              </Button>
            </div>
          ),
        },
      ]}
      data={roles}
    />
  );
}