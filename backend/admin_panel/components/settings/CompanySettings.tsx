"use client";

import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

export default function CompanySettings() {
  return (
    <div className="rounded-2xl border bg-white p-6 shadow-sm">
        
      <h2 className="mb-6 text-xl font-semibold">
        Organization Settings
      </h2>

      <div className="space-y-5">

        <div>
          <Label>Organization Name</Label>
          <Input
            placeholder="Acme Technologies Pvt Ltd"
            className="mt-2"
          />
        </div>

        <div>
          <Label>Email</Label>
          <Input
            type="email"
            placeholder="admin@company.com"
            className="mt-2"
          />
        </div>

        <div>
          <Label>Website</Label>
          <Input
            placeholder="https://company.com"
            className="mt-2"
          />
        </div>

        <Button>
          Save Changes
        </Button>

      </div>

    </div>
  );
}