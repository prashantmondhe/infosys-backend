"use client";
export {};
import { useEffect, useState } from "react";
import { toast } from "sonner";

import DataTable from "@/components/common/DataTable";
import StatusBadge from "@/components/common/StatusBadge";
import { Button } from "@/components/ui/button";

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";

import {
  Eye,
  Trash2,
  TriangleAlert,
} from "lucide-react";

import {
  getUsers,
  deleteUser,
} from "@/lib/api/api";

type Props = {
  search: string;
  department: string;
  role: string;
};

type User = {
  id: number;
  name: string;
  email: string;
  department: string;
  role: string;
  is_active: boolean;
};

export default function UsersTable({
  search,
  department,
  role,
}: Props) {

  console.log("========== UsersTable Rendered ==========");

  const [users, setUsers] = useState<User[]>([]);

  const loadUsers = async () => {
    console.log("========== loadUsers() CALLED ==========");

    try {
      const data = await getUsers();

      console.log("API Response:", data);
      console.log("Users Count:", data.length);

      setUsers(data);

      console.log("setUsers() Executed");
    } catch (error) {
      console.error("loadUsers Error:", error);
      toast.error("Failed to load users");
    }
  };

  useEffect(() => {
    console.log("========== useEffect Executed ==========");

    loadUsers();

    return () => {
      console.log("========== UsersTable Unmounted ==========");
    };
  }, []);

  const handleDelete = async (id: number) => {
    try {
      await deleteUser(id);

      toast.success("User deleted successfully");

      await loadUsers();
    } catch (error: any) {
      console.error(error);

      toast.error(error.message || "Failed to delete user");
    }
  };

  const filteredUsers = users.filter((user) => {
    const matchesSearch =
      user.name.toLowerCase().includes(search.toLowerCase()) ||
      user.email.toLowerCase().includes(search.toLowerCase());

    const matchesDepartment =
      department === "" || user.department === department;

    const matchesRole =
      role === "" || user.role === role;

    return (
      matchesSearch &&
      matchesDepartment &&
      matchesRole
    );
  });

  return (
    <DataTable
      columns={[
        {
          key: "name",
          label: "Employee",
        },
        {
          key: "email",
          label: "Email",
        },
        {
          key: "department",
          label: "Department",
        },
        {
          key: "role",
          label: "Role",
        },
        {
          key: "is_active",
          label: "Status",
          render: (value) => (
            <StatusBadge
              status={value ? "Active" : "Inactive"}
            />
          ),
        },
        {
          key: "id",
          label: "Actions",
          render: (value) => (
            <div className="flex gap-2">
              <Button
                size="icon"
                variant="ghost"
              >
                <Eye className="h-4 w-4" />
              </Button>

              <AlertDialog>
                <AlertDialogTrigger asChild>
                  <Button
                    size="icon"
                    variant="ghost"
                  >
                    <Trash2 className="h-4 w-4 text-red-500" />
                  </Button>
                </AlertDialogTrigger>

                <AlertDialogContent className="max-w-md rounded-3xl border shadow-2xl p-8">
                  <AlertDialogHeader className="items-center text-center">
                    <div className="mb-4 flex h-20 w-20 items-center justify-center rounded-full bg-red-100">
                      <TriangleAlert className="h-10 w-10 text-red-600" />
                    </div>

                    <AlertDialogTitle className="text-2xl font-bold">
                      Delete User
                    </AlertDialogTitle>

                    <AlertDialogDescription className="mt-2 text-base">
                      Are you sure you want to delete this user?
                      <br />
                      This action cannot be undone.
                    </AlertDialogDescription>
                  </AlertDialogHeader>

                  <AlertDialogFooter className="mt-6 gap-3">
                    <AlertDialogCancel>
                      Cancel
                    </AlertDialogCancel>

                    <AlertDialogAction
                      className="bg-violet-600 hover:bg-violet-700"
                      onClick={() => handleDelete(value as number)}
                    >
                      Delete User
                    </AlertDialogAction>
                  </AlertDialogFooter>
                </AlertDialogContent>
              </AlertDialog>
            </div>
          ),
        },
      ]}
      data={filteredUsers}
    />
  );
}