"use client";

import { useState } from "react";

import AnimatedContainer from "@/components/common/AnimatedContainer";
import PageHeader from "@/components/common/PageHeader";
import UserFilters from "@/components/users/UserFilters";
import UsersTable from "@/components/users/UsersTable";
import AddUserModal from "@/components/users/AddUserModal";

import { Button } from "@/components/ui/button";
import { UserPlus } from "lucide-react";

export default function UsersPage() {
  const [search, setSearch] = useState("");
  const [department, setDepartment] = useState("");
  const [role, setRole] = useState("");

  const [userOpen, setUserOpen] = useState(false);

  return (
    <>
      <AnimatedContainer>
        <div className="space-y-6">

          <div className="flex items-center justify-between">

            <PageHeader
              title="Users"
              description="Manage employees and their departments."
            />

            <Button
              onClick={() => setUserOpen(true)}
              className="bg-violet-600 hover:bg-violet-700"
            >
              <UserPlus className="mr-2 h-4 w-4" />
              Add User
            </Button>

          </div>

          <UserFilters
            search={search}
            setSearch={setSearch}
            department={department}
            setDepartment={setDepartment}
            role={role}
            setRole={setRole}
          />

          <UsersTable
            search={search}
            department={department}
            role={role}
          />

        </div>
      </AnimatedContainer>

      <AddUserModal
        open={userOpen}
        onOpenChange={setUserOpen}
      />
    </>
  );
}