"use client";

interface Props {
  search: string;
  setSearch: (value: string) => void;

  status: string;
  setStatus: (value: string) => void;
}

import { Search } from "lucide-react";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function DepartmentFilters({
  search,
  setSearch,
  status,
  setStatus,
}: Props) {
  return (
    <div className="flex flex-wrap items-center gap-4 rounded-2xl border bg-card p-5 shadow-sm">

      <div className="relative flex-1 min-w-72">

        <Search className="absolute left-3 top-3 h-4 w-4 text-slate-400" />

        <Input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search department..."
          className="pl-10 rounded-xl"
        />

      </div>

      <select
        value={status}
        onChange={(e) => setStatus(e.target.value)}
        className="h-10 rounded-xl border px-4"
      >
        <option value="All">All Status</option>
        <option value="Active">Active</option>
        <option value="Inactive">Inactive</option>
      </select>

      <Button
        variant="outline"
        onClick={() => {
          setSearch("");
          setStatus("All");
        }}
      >
        Reset
      </Button>

    </div>
  );
}