import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

interface Column<T> {
  key: keyof T;
  label: string;
  render?: (value: unknown, row: T) => React.ReactNode;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
}

export default function DataTable<T extends { id: number | string }>({
  columns,
  data,
}: DataTableProps<T>) {
  return (
    <div className="overflow-hidden rounded-2xl border border-border bg-card shadow-sm">
      <Table>
        <TableHeader className="bg-muted">
          <TableRow className="border-border">
            {columns.map((column) => (
              <TableHead
                key={String(column.key)}
                className="font-semibold text-foreground"
              >
                {column.label}
              </TableHead>
            ))}
          </TableRow>
        </TableHeader>

        <TableBody>
          {data.map((row) => (
            <TableRow
              key={row.id}
              className="border-border transition-colors hover:bg-muted/50"
            >
              {columns.map((column) => (
                <TableCell
                  key={String(column.key)}
                  className="text-foreground"
                >
                  {column.render
                    ? column.render(row[column.key], row)
                    : String(row[column.key])}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}