"use client";

import { useState } from "react";
import { Plus } from "lucide-react";
import { toast } from "sonner";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
  DialogTrigger,
} from "@/components/ui/dialog";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import { createDepartment } from "@/lib/api/api";

export default function AddDepartmentModal() {
  const [open, setOpen] = useState(false);

  const [name, setName] = useState("");
  const [departmentHead, setDepartmentHead] = useState("");

  const handleSave = async () => {
    if (!name || !departmentHead) {
      toast.error("Please fill all fields");
      return;
    }

    try {
      await createDepartment({
        name,
        department_head: departmentHead,
        is_active: true,
      });

      toast.success("Department created successfully");

      setName("");
      setDepartmentHead("");

      setOpen(false);

      window.location.reload();
    } catch (error) {
      console.error(error);
      toast.error("Failed to create department");
    }
  };

  return (
    <Dialog
      open={open}
      onOpenChange={setOpen}
    >
      <DialogTrigger
        className="
          inline-flex
          h-10
          items-center
          justify-center
          rounded-xl
          bg-violet-600
          px-4
          text-sm
          font-medium
          text-white
          transition-colors
          hover:bg-violet-700
        "
      >
        <Plus className="mr-2 h-4 w-4" />
        Add Department
      </DialogTrigger>

      <DialogContent className="max-w-lg rounded-2xl">

        <DialogHeader>

          <DialogTitle className="text-2xl font-bold">
            Add Department
          </DialogTitle>

        </DialogHeader>

        <div className="space-y-5 py-4">

          <Input
            placeholder="Department Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />

          <Input
            placeholder="Department Head"
            value={departmentHead}
            onChange={(e) => setDepartmentHead(e.target.value)}
          />

        </div>

        <DialogFooter className="gap-3">

          <Button
            variant="outline"
            onClick={() => setOpen(false)}
          >
            Cancel
          </Button>

          <Button
            className="bg-violet-600 hover:bg-violet-700"
            onClick={handleSave}
          >
            Save Department
          </Button>

        </DialogFooter>

      </DialogContent>
    </Dialog>
  );
}