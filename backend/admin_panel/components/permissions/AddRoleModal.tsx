"use client";

import { Plus } from "lucide-react";

import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function AddRoleModal() {
  return (
    <Dialog>
      <DialogTrigger
        className="
          inline-flex
          h-10
          items-center
          justify-center
          rounded-lg
          bg-primary
          px-4
          text-sm
          font-medium
          text-primary-foreground
          transition-colors
          hover:bg-primary/90
        "
      >
        <Plus className="mr-2 h-4 w-4" />
        Add Role
      </DialogTrigger>

      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create Role</DialogTitle>
        </DialogHeader>

        <div className="space-y-4 py-4">
          <Input placeholder="Role Name" />

          <div className="grid grid-cols-2 gap-3">
            <label className="flex items-center gap-2">
              <input type="checkbox" />
              Dashboard
            </label>

            <label className="flex items-center gap-2">
              <input type="checkbox" />
              Documents
            </label>

            <label className="flex items-center gap-2">
              <input type="checkbox" />
              Users
            </label>

            <label className="flex items-center gap-2">
              <input type="checkbox" />
              Departments
            </label>

            <label className="flex items-center gap-2">
              <input type="checkbox" />
              Reports
            </label>

            <label className="flex items-center gap-2">
              <input type="checkbox" />
              Storage
            </label>

            <label className="flex items-center gap-2">
              <input type="checkbox" />
              Activity Logs
            </label>

            <label className="flex items-center gap-2">
              <input type="checkbox" />
              Settings
            </label>
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline">
            Cancel
          </Button>

          <Button>
            Save Role
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}