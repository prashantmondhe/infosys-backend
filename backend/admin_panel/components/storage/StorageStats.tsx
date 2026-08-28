"use client";

import {
  HardDrive,
  FileText,
  Image,
  FolderOpen,
} from "lucide-react";

const stats = [
  {
    title: "Total Storage",
    value: "256 GB",
    icon: HardDrive,
  },
  {
    title: "Documents",
    value: "1,245",
    icon: FileText,
  },
  {
    title: "Images",
    value: "3,487",
    icon: Image,
  },
  {
    title: "Folders",
    value: "186",
    icon: FolderOpen,
  },
];

export default function StorageStats() {
  return (
    <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">

      {stats.map((item) => {
        const Icon = item.icon;

        return (
          <div
            key={item.title}
            className="rounded-2xl border bg-white p-6 shadow-sm"
          >
            <div className="flex items-center justify-between">

              <div>
                <p className="text-sm text-muted-foreground">
                  {item.title}
                </p>

                <h2 className="mt-2 text-3xl font-bold">
                  {item.value}
                </h2>
              </div>

              <div className="rounded-xl bg-primary/10 p-3">
                <Icon className="h-6 w-6 text-primary" />
              </div>

            </div>
          </div>
        );
      })}

    </div>
  );
}