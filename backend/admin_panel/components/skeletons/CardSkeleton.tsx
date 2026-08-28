import { Skeleton } from "@/components/ui/skeleton";

export default function CardSkeleton() {
  return (
    <div className="rounded-2xl border bg-background p-6 shadow-sm">
      <div className="flex items-center justify-between">

        <div className="space-y-3">
          <Skeleton className="h-4 w-24" />
          <Skeleton className="h-8 w-32" />
          <Skeleton className="h-3 w-20" />
        </div>

        <Skeleton className="h-14 w-14 rounded-xl" />

      </div>
    </div>
  );
}