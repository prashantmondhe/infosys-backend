import { Skeleton } from "@/components/ui/skeleton";

export default function ChatSkeleton() {
  return (
    <div className="space-y-6">

      {Array.from({ length: 6 }).map((_, index) => (
        <div
          key={index}
          className={`flex ${
            index % 2 === 0 ? "justify-start" : "justify-end"
          }`}
        >
          <Skeleton className="h-24 w-[70%] rounded-2xl" />
        </div>
      ))}

    </div>
  );
}