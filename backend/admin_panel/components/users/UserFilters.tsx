"use client";

import { useEffect, useState } from "react";

import SearchFilter from "@/components/common/SearchFilter";
import { getDepartments } from "@/lib/api/api";

type Department = {
  id: number;
  name: string;
  is_active: boolean;
};

type Props = {
  search: string;
  setSearch: React.Dispatch<React.SetStateAction<string>>;

  department: string;
  setDepartment: React.Dispatch<React.SetStateAction<string>>;

  role: string;
  setRole: React.Dispatch<React.SetStateAction<string>>;
};

export default function UserFilters({
  search,
  setSearch,
  department,
  setDepartment,
  role,
  setRole,
}: Props) {
  const [departments, setDepartments] = useState<Department[]>([]);

  useEffect(() => {
    loadDepartments();
  }, []);

  const loadDepartments = async () => {
    try {
      const data = await getDepartments();

      // Show only active departments
      const activeDepartments = data.filter(
        (dept: Department) => dept.is_active
      );

      setDepartments(activeDepartments);
    } catch (error) {
      console.error("Failed to load departments:", error);
    }
  };

  return (
    <div className="flex flex-wrap items-center justify-between gap-4 rounded-2xl border bg-card p-5 shadow-sm">

      <SearchFilter
        placeholder="Search employee..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      <div className="flex gap-3">

        {/* Department Filter */}
        <select
          value={department}
          onChange={(e) => setDepartment(e.target.value)}
          className="h-10 rounded-xl border border-slate-300 px-4"
        >
          <option value="">All Departments</option>

          {departments.map((dept) => (
            <option key={dept.id} value={dept.name}>
              {dept.name}
            </option>
          ))}
        </select>

        {/* Role Filter */}
        <select
          value={role}
          onChange={(e) => setRole(e.target.value)}
          className="h-10 rounded-xl border border-slate-300 px-4"
        >
          <option value="">All Roles</option>
          <option value="Super Admin">Super Admin</option>
          <option value="Admin">Admin</option>
          <option value="Manager">Manager</option>
          <option value="Employee">Employee</option>
        </select>

      </div>

    </div>
  );
}