import { Button } from "@/components/ui/button";
import { Download, Upload } from "lucide-react";

export default function DashboardHeader() {
  return (
    <div className="flex items-center justify-between">
      <div>
        <h1 className="text-4xl font-bold tracking-tight text-foreground">
          Welcome back, Rohan 👋  
        </h1>

        <p className="mt-2 text-muted-foreground">
          Manage Documents, Departments & Permissions.
        </p>
      </div>

      {/* <div className="flex gap-3">
        <Button
          variant="outline"
          className="rounded-xl"
        >
          <Download className="mr-2 h-4 w-4" />
          Export
        </Button>

        <Button
          className="rounded-xl bg-primary text-primary-foreground hover:bg-primary/90"
        >
          <Upload className="mr-2 h-4 w-4" />
          Upload Document
        </Button>
      </div> */}
    </div>
  );
}