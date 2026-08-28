"use client";

import { Switch } from "@/components/ui/switch";

export default function AppearanceSettings() {
  return (
    <div className="rounded-2xl border bg-white p-6 shadow-sm">

      <h2 className="mb-6 text-xl font-semibold">
        Appearance
      </h2>

      <div className="space-y-6">

        <div className="flex items-center justify-between">

          <div>
            <h4 className="font-medium">
              Dark Mode
            </h4>

            <p className="text-sm text-muted-foreground">
              Enable dark theme.
            </p>
          </div>

          <Switch />
        </div>

        <div className="flex items-center justify-between">

          <div>
            <h4 className="font-medium">
              Compact Layout
            </h4>

            <p className="text-sm text-muted-foreground">
              Display more content on screen.
            </p>
          </div>

          <Switch />
        </div>

      </div>

    </div>
  );
}