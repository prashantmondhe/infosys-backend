"use client";

import DataTable from "@/components/common/DataTable";
import { Button } from "@/components/ui/button";
import {
  Download,
  Eye,
  Trash2,
} from "lucide-react";

type FileItem = {
  id: number;
  name: string;
  type: string;
  size: string;
  owner: string;
  uploaded: string;
};

const files: FileItem[] = [
  {
    id: 1,
    name: "Employee Handbook.pdf",
    type: "PDF",
    size: "2.4 MB",
    owner: "Admin",
    uploaded: "Today",
  },
  {
    id: 2,
    name: "Company Policy.docx",
    type: "DOCX",
    size: "1.8 MB",
    owner: "HR",
    uploaded: "Yesterday",
  },
  {
    id: 3,
    name: "Annual Report.xlsx",
    type: "XLSX",
    size: "4.7 MB",
    owner: "Finance",
    uploaded: "3 days ago",
  },
];

export default function StorageTable() {
  return (
    <DataTable
      columns={[
        {
          key: "name",
          label: "File Name",
        },
        {
          key: "type",
          label: "Type",
        },
        {
          key: "size",
          label: "Size",
        },
        {
          key: "owner",
          label: "Owner",
        },
        {
          key: "uploaded",
          label: "Uploaded",
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
                <Download className="h-4 w-4" />
              </Button>

              <Button size="icon" variant="ghost">
                <Trash2 className="h-4 w-4 text-red-500" />
              </Button>

            </div>
          ),
        },
      ]}
      data={files}
    />
  );
}