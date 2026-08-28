"use client";

import { useState } from "react";

import PageHeader from "@/components/common/PageHeader";
import DepartmentFilters from "@/components/departments/DepartmentFilters";
import DepartmentsTable from "@/components/departments/DepartmentTable";
import AddDepartmentModal from "@/components/departments/AddDepartmentModal";
import AnimatedContainer from "@/components/common/AnimatedContainer";

export default function DepartmentsPage() {
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("All");

  return (
    <AnimatedContainer>
      <div className="space-y-8">

        <div className="flex items-center justify-between">

          <PageHeader
            title="Departments"
            description="Manage departments and organizational structure."
          />

          <AddDepartmentModal />

        </div>

        <DepartmentFilters
          search={search}
          setSearch={setSearch}
          status={status}
          setStatus={setStatus}
        />

        <DepartmentsTable
          search={search}
          status={status}
        />

      </div>
    </AnimatedContainer>
  );
}