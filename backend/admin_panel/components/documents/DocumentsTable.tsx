"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";

import { Eye, Trash2, TriangleAlert } from "lucide-react";

import DataTable from "@/components/common/DataTable";
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
  getDocuments,
  deleteDocument,
} from "@/lib/api/api";

type Document = {
  id: number;
  title: string;
  file_name: string;
  file_path: string;
  uploaded_by: string;
  department: string;
  created_at: string;
};

type Props = {
  search: string;
  department: string;
};

export default function DocumentsTable({
  search,
  department,
}: Props) {
  const [documents, setDocuments] = useState<Document[]>([]);

  const loadDocuments = async () => {
    try {
      const data = await getDocuments();
      setDocuments(data);
    } catch (error) {
      console.error(error);
      toast.error("Failed to load documents");
    }
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  const handleDelete = async (id: number) => {
    try {
      await deleteDocument(id);

      toast.success("Document deleted successfully");

      await loadDocuments();
    } catch (error) {
      console.error(error);
      toast.error("Failed to delete document");
    }
  };

  const filteredDocuments = documents.filter((doc) => {
    const matchesSearch = doc.title
      .toLowerCase()
      .includes(search.toLowerCase());

    const matchesDepartment =
      department === "All" ||
      doc.department === department;

    return matchesSearch && matchesDepartment;
  });

  return (
    <DataTable
      columns={[
        {
          key: "title",
          label: "Document",
        },
        {
          key: "department",
          label: "Department",
        },
        {
          key: "uploaded_by",
          label: "Uploaded By",
        },
        {
          key: "created_at",
          label: "Uploaded On",
          render: (value) =>
            new Date(value as string).toLocaleString(),
        },
        {
          key: "id",
          label: "Actions",
          render: (value) => {
            const document = documents.find(
              (doc) => doc.id === value
            );

            return (
              <div className="flex gap-2">

                <Button
                  size="icon"
                  variant="ghost"
                  onClick={() => {
                    if (document) {
                      window.open(
                        `http://localhost:8000/${document.file_path}`,
                        "_blank"
                      );
                    }
                  }}
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
                        Delete Document
                      </AlertDialogTitle>

                      <AlertDialogDescription className="mt-2 text-base">
                        Are you sure you want to delete this document?
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
                        Delete Document
                      </AlertDialogAction>

                    </AlertDialogFooter>

                  </AlertDialogContent>

                </AlertDialog>

              </div>
            );
          },
        },
      ]}
      data={filteredDocuments}
    />
  );
}