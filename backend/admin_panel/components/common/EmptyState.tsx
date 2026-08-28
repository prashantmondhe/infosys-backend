"use client";

import { ReactNode } from "react";
import { Inbox } from "lucide-react";
import { Button } from "@/components/ui/button";

interface EmptyStateProps {
  icon?: ReactNode;
  title: string;
  description: string;
  buttonText?: string;
  onButtonClick?: () => void;
}

export default function EmptyState({
  icon,
  title,
  description,
  buttonText,
  onButtonClick,
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center rounded-2xl border border-dashed bg-background px-6 py-16 text-center">

      <div className="mb-5 rounded-full bg-primary/10 p-5">
        {icon ?? (
          <Inbox className="h-10 w-10 text-primary" />
        )}
      </div>

      <h2 className="text-2xl font-semibold">
        {title}
      </h2>

      <p className="mt-2 max-w-md text-muted-foreground">
        {description}
      </p>

      {buttonText && (
        <Button
          className="mt-8"
          onClick={onButtonClick}
        >
          {buttonText}
        </Button>
      )}

    </div>
  );
}