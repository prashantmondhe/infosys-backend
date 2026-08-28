"use client";

import { Switch } from "@/components/ui/switch";

export default function SecuritySettings() {
  return (
    <div className="rounded-2xl border bg-white p-6 shadow-sm">

      <h2 className="mb-6 text-xl font-semibold">
        Security
      </h2>

      <div className="space-y-6">

        <div className="flex items-center justify-between">

          <div>
            <h4 className="font-medium">
              Two-Factor Authentication
            </h4>

            <p className="text-sm text-muted-foreground">
              Require administrators to verify using OTP.
            </p>
          </div>

          <Switch />
        </div>

        <div className="flex items-center justify-between">

          <div>
            <h4 className="font-medium">
              Session Timeout
            </h4>

            <p className="text-sm text-muted-foreground">
              Automatically logout inactive users.
            </p>
          </div>

          <Switch />
        </div>

      </div>

    </div>
  );
}