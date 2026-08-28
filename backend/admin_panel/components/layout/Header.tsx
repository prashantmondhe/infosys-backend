"use client";

import { Bell, Search, Settings } from "lucide-react";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import ThemeToggle from "@/components/common/ThemeToggle";

export default function Header() {
  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b bg-background px-6">

      {/* Left */}

      <div className="relative w-80">

        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />

        <Input
          placeholder="Search..."
          className="pl-10"
        />

      </div>

      {/* Right */}

      <div className="flex items-center gap-2">

        <ThemeToggle />

        <Button
          variant="ghost"
          size="icon"
        >
          <Bell className="h-5 w-5" />
        </Button>

        <Button
          variant="ghost"
          size="icon"
        >
          <Settings className="h-5 w-5" />
        </Button>

        <div className="ml-2 flex items-center gap-3">

          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary text-sm font-semibold text-primary-foreground">
            RB
          </div>

          <div className="hidden sm:block">
            <p className="text-sm font-medium">
              Rohan Bhesara
            </p>

            <p className="text-xs text-muted-foreground">
              Super Admin
            </p>
          </div>

        </div>

      </div>

    </header>
  );
}