"use client";

import { Search } from "lucide-react";
import { Input } from "@/components/ui/input";
import { ChangeEvent } from "react";

interface Props {
  placeholder?: string;
  value: string;
  onChange: (e: ChangeEvent<HTMLInputElement>) => void;
}

export default function SearchFilter({
  placeholder = "Search...",
  value,
  onChange,
}: Props) {
  return (
    <div className="relative w-full max-w-md">

      <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />

      <Input
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        className="pl-10 rounded-xl"
      />

    </div>
  );
}