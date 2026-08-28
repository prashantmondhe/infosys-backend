"use client";

import { useState, useEffect } from "react";
import { Upload } from "lucide-react";
import { toast } from "sonner";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import {
  createDocument,
  getDepartments,
} from "@/lib/api/api";

type Department = {
  id: number;
  name: string;
};

export default function UploadDocumentModal() {
  const [open, setOpen] = useState(false);

  const [title, setTitle] = useState("");
  const [departmentId, setDepartmentId] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const [departments, setDepartments] = useState<Department[]>([]);

  useEffect(() => {
    const loadDepartments = async () => {
      try {
        const data = await getDepartments();

        setDepartments(data);

        if (data.length > 0) {
          setDepartmentId(data[0].id.toString());
        }
      } catch (error) {
        console.error(error);
        toast.error("Failed to load departments.");
      }
    };

    loadDepartments();
  }, []);

  const handleUpload = async () => {
    if (!title || !selectedFile || !departmentId) {
      toast.error("Please fill all required fields.");
      return;
    }

    try {
      const formData = new FormData();

      formData.append("title", title);
      formData.append("department_id", departmentId);
      formData.append("uploaded_by", "1"); // Replace later with logged-in user
      formData.append("file", selectedFile);

      await createDocument(formData);

      toast.success("Document uploaded successfully.");

      setTitle("");
      setSelectedFile(null);

      if (departments.length > 0) {
        setDepartmentId(departments[0].id.toString());
      }

      setOpen(false);

      window.location.reload();
    } catch (error) {
      console.error(error);
      toast.error("Failed to upload document.");
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <Button
        className="rounded-xl bg-violet-600 hover:bg-violet-700"
        onClick={() => setOpen(true)}
      >
        <Upload className="mr-2 h-4 w-4" />
        Upload Document
      </Button>

      <DialogContent className="max-w-xl">
        <DialogHeader>
          <DialogTitle className="text-2xl">
            Upload Document
          </DialogTitle>
        </DialogHeader>

        <div className="mt-6 space-y-5">

          <Input
            placeholder="Document Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />

          <Input
            type="file"
            accept=".pdf,.doc,.docx"
            onChange={(e) => {
              if (e.target.files?.length) {
                setSelectedFile(e.target.files[0]);
              }
            }}
          />

          <select
            value={departmentId}
            onChange={(e) => setDepartmentId(e.target.value)}
            className="h-11 w-full rounded-xl border px-4"
          >
            {departments.map((dept) => (
              <option
                key={dept.id}
                value={dept.id}
              >
                {dept.name}
              </option>
            ))}
          </select>

          <div className="flex justify-end gap-3">
            <Button
              variant="outline"
              onClick={() => setOpen(false)}
            >
              Cancel
            </Button>

            <Button
              className="bg-violet-600 hover:bg-violet-700"
              onClick={handleUpload}
            >
              Upload Document
            </Button>
          </div>

        </div>
      </DialogContent>
    </Dialog>
  );
}