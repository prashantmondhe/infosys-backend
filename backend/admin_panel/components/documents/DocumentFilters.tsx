"use client";

import { useEffect, useState } from "react";
import { Search } from "lucide-react";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

import { getDepartments } from "@/lib/api/api";

type Department = {
  id: number;
  name: string;
};

type Props = {
  search: string;
  setSearch: (value: string) => void;

  department: string;
  setDepartment: (value: string) => void;

  resetFilters: () => void;
};

export default function DocumentFilters({
  search,
  setSearch,
  department,
  setDepartment,
  resetFilters,
}: Props) {
  const [departments, setDepartments] = useState<Department[]>([]);

  useEffect(() => {
    const loadDepartments = async () => {
      try {
        const data = await getDepartments();
        setDepartments(data);
      } catch (error) {
        console.error("Failed to load departments:", error);
      }
    };

    loadDepartments();
  }, []);

  return (
    <div className="flex flex-wrap items-center gap-4 rounded-2xl border bg-card p-5 shadow-sm">
      <div className="relative flex-1 min-w-[300px]">
        <Search className="absolute left-3 top-3 h-4 w-4 text-slate-400" />

        <Input
          placeholder="Search document..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="pl-10 rounded-xl"
        />
      </div>

      <select
        value={department}
        onChange={(e) => setDepartment(e.target.value)}
        className="h-10 rounded-xl border border-slate-300 px-4"
      >
        <option value="">All Departments</option>

        {departments.map((dept) => (
          <option
            key={dept.id}
            value={dept.name} // <-- Changed from ID to Name
          >
            {dept.name}
          </option>
        ))}
      </select>

      <Button
        variant="outline"
        onClick={resetFilters}
      >
        Reset
      </Button>
    </div>
  );
}