"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";

import DataTable from "@/components/common/DataTable";
import StatusBadge from "@/components/common/StatusBadge";
import { Button } from "@/components/ui/button";

import {
  Eye,
  Trash2,
  TriangleAlert,
} from "lucide-react";

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
  getDepartments,
  deleteDepartment,
} from "@/lib/api/api";

type Department = {
  id: number;
  name: string;
  department_head: string;
  is_active: boolean;
};

type Props = {
  search: string;
  status: string;
};

export default function DepartmentsTable({
  search,
  status,
}: Props) {
  const [departments, setDepartments] = useState<Department[]>([]);

  const loadDepartments = async () => {
    try {
      const data = await getDepartments();
      setDepartments(data);
    } catch (error) {
      console.error(error);
      toast.error("Failed to load departments");
    }
  };

  useEffect(() => {
    loadDepartments();
  }, []);

  const handleDelete = async (id: number) => {
    try {
      await deleteDepartment(id);

      toast.success("Department deleted successfully");

      await loadDepartments();
    } catch (error) {
      console.error(error);

      if (error instanceof Error) {
        toast.error(error.message);
      } else {
        toast.error("Failed to delete department");
      }
    }
  };

  const filteredDepartments = departments.filter((department) => {
    const matchesSearch =
      department.name
        .toLowerCase()
        .includes(search.toLowerCase()) ||
      department.department_head
        .toLowerCase()
        .includes(search.toLowerCase());

    const matchesStatus =
      status === "All" ||
      (status === "Active" && department.is_active) ||
      (status === "Inactive" && !department.is_active);

    return matchesSearch && matchesStatus;
  });

  return (
    <DataTable
      columns={[
        {
          key: "name",
          label: "Department",
        },
        {
          key: "department_head",
          label: "Department Head",
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

                    <div className="mb-4 flex h-20 w-20 items-center justify-center rounded-full bg-red-100 dark:bg-red-900/30">

                      <TriangleAlert className="h-10 w-10 text-red-600" />

                    </div>

                    <AlertDialogTitle className="text-2xl font-bold">
                      Delete Department
                    </AlertDialogTitle>

                    <AlertDialogDescription className="mt-2 text-base leading-6">
                      Are you sure you want to delete this department?
                      <br />
                      This action cannot be undone.
                    </AlertDialogDescription>

                  </AlertDialogHeader>

                  <AlertDialogFooter className="mt-6 gap-3">

                    <AlertDialogCancel className="rounded-xl">
                      Cancel
                    </AlertDialogCancel>

                    <AlertDialogAction
                      className="rounded-xl bg-violet-600 hover:bg-violet-700 text-white"
                      onClick={() => handleDelete(value as number)}
                    >
                      Delete Department
                    </AlertDialogAction>

                  </AlertDialogFooter>

                </AlertDialogContent>

              </AlertDialog>

            </div>
          ),
        },
      ]}
      data={filteredDepartments}
    />
  );
}