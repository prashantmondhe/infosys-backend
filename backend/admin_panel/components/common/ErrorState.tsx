"use client";

import { AlertTriangle } from "lucide-react";
import { Button } from "@/components/ui/button";

interface ErrorStateProps {
  title?: string;
  description?: string;
  buttonText?: string;
  onRetry?: () => void;
}

export default function ErrorState({
  title = "Something went wrong",
  description = "We couldn't load the requested data. Please try again.",
  buttonText = "Try Again",
  onRetry,
}: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center rounded-2xl border border-dashed bg-background px-6 py-16 text-center">

      <div className="mb-5 rounded-full bg-red-100 p-5 dark:bg-red-500/10">
        <AlertTriangle className="h-10 w-10 text-red-600 dark:text-red-400" />
      </div>

      <h2 className="text-2xl font-semibold">
        {title}
      </h2>

      <p className="mt-2 max-w-md text-muted-foreground">
        {description}
      </p>

      <Button
        className="mt-8"
        onClick={onRetry}
      >
        {buttonText}
      </Button>

    </div>
  );
}