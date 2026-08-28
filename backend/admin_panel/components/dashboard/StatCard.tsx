import { Card } from "@/components/ui/card";
import { LucideIcon, TrendingUp } from "lucide-react";

interface Props {
  title: string;
  value: string;
  change: string;
  icon: LucideIcon;
}

export default function StatCard({
  title,
  value,
  change,
  icon: Icon,
}: Props) {
  return (
    <Card
      className="
        group
        overflow-hidden
        rounded-2xl
        border
        border-border
        bg-card
        p-6
        shadow-sm
        transition-all
        duration-300
        hover:-translate-y-1
        hover:border-primary/40
        hover:shadow-xl
      "
    >
      <div className="flex items-start justify-between">
        <div className="space-y-5">
          <div>
            <p className="text-sm font-medium uppercase tracking-wide text-muted-foreground">
              {title}
            </p>

            <h2 className="mt-3 text-5xl font-bold tracking-tight text-card-foreground">
              {value}
            </h2>
          </div>

          <div className="inline-flex items-center gap-2 rounded-full bg-green-500/10 px-3 py-1">
            <TrendingUp className="h-4 w-4 text-green-600 dark:text-green-400" />

            <span className="text-sm font-semibold text-green-600 dark:text-green-400">
              {change}
            </span>

            <span className="text-xs text-muted-foreground">
              vs last month
            </span>
          </div>
        </div>

        <div
          className="
            flex
            h-16
            w-16
            items-center
            justify-center
            rounded-2xl
            bg-gradient-to-br
            from-violet-500
            via-violet-600
            to-indigo-600
            shadow-lg
            shadow-violet-500/25
            transition-all
            duration-300
            group-hover:scale-110
            group-hover:rotate-6
          "
        >
          <Icon className="h-8 w-8 text-white" />
        </div>
      </div>
    </Card>
  );
}