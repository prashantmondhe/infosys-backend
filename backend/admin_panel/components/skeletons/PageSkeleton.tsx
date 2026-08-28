import { Skeleton } from "@/components/ui/skeleton";
import TableSkeleton from "./TableSkeleton";

export default function PageSkeleton() {
  return (
    <div className="space-y-8">

      <div className="space-y-3">

        <Skeleton className="h-8 w-52" />

        <Skeleton className="h-4 w-80" />

      </div>

      <div className="flex justify-between rounded-2xl border bg-background p-5">

        <Skeleton className="h-10 w-64" />

        <Skeleton className="h-10 w-40" />

      </div>

      <TableSkeleton />

    </div>
  );
}