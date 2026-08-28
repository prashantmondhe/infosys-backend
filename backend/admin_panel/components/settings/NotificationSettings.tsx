"use client";

import { Switch } from "@/components/ui/switch";

export default function NotificationSettings() {
  return (
    <div className="rounded-2xl border bg-white p-6 shadow-sm">

      <h2 className="mb-6 text-xl font-semibold">
        Notifications
      </h2>

      <div className="space-y-6">

        <div className="flex items-center justify-between">

          <div>
            <h4 className="font-medium">
              Email Notifications
            </h4>

            <p className="text-sm text-muted-foreground">
              Receive updates through email.
            </p>
          </div>

          <Switch />
        </div>

        <div className="flex items-center justify-between">

          <div>
            <h4 className="font-medium">
              Document Alerts
            </h4>

            <p className="text-sm text-muted-foreground">
              Notify when documents are uploaded.
            </p>
          </div>

          <Switch />
        </div>

      </div>

    </div>
  );
}