import { Skeleton } from "@/components/ui/skeleton";

interface Props {
  rows?: number;
  columns?: number;
}

export default function TableSkeleton({
  rows = 8,
  columns = 6,
}: Props) {
  return (
    <div className="overflow-hidden rounded-2xl border bg-background shadow-sm">

      <div className="border-b p-4">
        <Skeleton className="h-6 w-52" />
      </div>

      <div className="overflow-x-auto">

        <table className="w-full">

          <thead>

            <tr className="border-b">

              {Array.from({ length: columns }).map((_, index) => (
                <th key={index} className="p-4">
                  <Skeleton className="h-4 w-24" />
                </th>
              ))}

            </tr>

          </thead>

          <tbody>

            {Array.from({ length: rows }).map((_, row) => (
              <tr key={row} className="border-b">

                {Array.from({ length: columns }).map((_, col) => (
                  <td key={col} className="p-4">
                    <Skeleton className="h-4 w-full max-w-[140px]" />
                  </td>
                ))}

              </tr>
            ))}

          </tbody>

        </table>

      </div>

    </div>
  );
}