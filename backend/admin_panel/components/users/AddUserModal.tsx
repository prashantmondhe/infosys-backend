"use client";

import { useState } from "react";
import { toast } from "sonner";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import { createUser } from "@/lib/api/api";

type Props = {
  open: boolean;
  onOpenChange: (open: boolean) => void;
};

export default function AddUserModal({
  open,
  onOpenChange,
}: Props) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [department, setDepartment] = useState("");
  const [role, setRole] = useState("");

  const handleSave = async () => {
    if (!name || !email || !department || !role) {
      toast.warning("Please fill all fields");
      return;
    }

    try {
      await createUser({
        name,
        email,
        department,
        role,
      });

      toast.success("User Added Successfully");

      setName("");
      setEmail("");
      setDepartment("");
      setRole("");

      onOpenChange(false);

      window.location.reload();
    } catch (err) {
      console.error(err);
      toast.error("Failed to add user");
    }
  };

  return (
    <Dialog
      open={open}
      onOpenChange={onOpenChange}
    >
      <DialogContent className="max-w-xl">
        <DialogHeader>
          <DialogTitle>Add Employee</DialogTitle>
        </DialogHeader>

        <div className="mt-4 space-y-4">

          <Input
            placeholder="Full Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />

          <Input
            placeholder="Email Address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <select
            className="h-11 w-full rounded-xl border px-4"
            value={department}
            onChange={(e) => setDepartment(e.target.value)}
          >
            <option value="">Select Department</option>
            <option>Admin</option>
            <option>HR</option>
            <option>Sales</option>
            <option>Finance</option>
            <option>IT</option>
          </select>

          <select
            className="h-11 w-full rounded-xl border px-4"
            value={role}
            onChange={(e) => setRole(e.target.value)}
          >
            <option value="">Select Role</option>
            <option>Super Admin</option>
            <option>Admin</option>
            <option>Manager</option>
            <option>Employee</option>
          </select>

          <div className="flex justify-end gap-3">
            <Button
              variant="outline"
              onClick={() => onOpenChange(false)}
            >
              Cancel
            </Button>

            <Button
              onClick={handleSave}
              className="bg-violet-600 hover:bg-violet-700"
            >
              Save User
            </Button>
          </div>

        </div>
      </DialogContent>
    </Dialog>
  );
}