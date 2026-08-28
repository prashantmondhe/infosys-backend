import CardSkeleton from "./CardSkeleton";
import TableSkeleton from "./TableSkeleton";

export default function DashboardSkeleton() {
  return (
    <div className="space-y-8">

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">

        <CardSkeleton />
        <CardSkeleton />
        <CardSkeleton />
        <CardSkeleton />

      </div>

      <TableSkeleton rows={6} columns={5} />

    </div>
  );
}