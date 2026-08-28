"use client";

import { useState } from "react";

import DocumentHeader from "@/components/documents/DocumentHeader";
import DocumentFilters from "@/components/documents/DocumentFilters";
import DocumentsTable from "@/components/documents/DocumentsTable";
import AnimatedContainer from "@/components/common/AnimatedContainer";

export default function DocumentsPage() {
  const [search, setSearch] = useState("");
  const [department, setDepartment] = useState("All");

  const resetFilters = () => {
    setSearch("");
    setDepartment("All");
  };

  return (
    <AnimatedContainer>
      <div className="space-y-8">

        <DocumentHeader />

        <DocumentFilters
          search={search}
          setSearch={setSearch}
          department={department}
          setDepartment={setDepartment}
          resetFilters={resetFilters}
        />

        <DocumentsTable
          search={search}
          department={department}
        />

      </div>
    </AnimatedContainer>
  );
}