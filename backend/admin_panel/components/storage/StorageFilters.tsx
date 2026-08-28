"use client";

import SearchFilter from "@/components/common/SearchFilter";

export default function StorageFilters() {
  return (
    <div className="flex flex-wrap items-center justify-between gap-4 rounded-2xl border bg-white p-5 shadow-sm">

      <SearchFilter placeholder="Search files..." />

      <select className="h-10 rounded-xl border px-4">
        <option>All File Types</option>
        <option>PDF</option>
        <option>DOCX</option>
        <option>PNG</option>
        <option>JPG</option>
        <option>XLSX</option>
      </select>

    </div>
  );
}