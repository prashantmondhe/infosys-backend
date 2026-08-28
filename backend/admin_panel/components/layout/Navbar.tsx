"use client";

import { Bell, Search, CalendarDays } from "lucide-react";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import ThemeToggle from "@/components/common/ThemeToggle";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 h-20 border-b border-border bg-background/90 backdrop-blur-md">
      <div className="flex h-full items-center justify-between px-8">
        {/* Left */}
        <div>
          <h2 className="text-2xl font-bold text-foreground">
            Dashboard
          </h2>

          <p className="text-sm text-muted-foreground">
            Welcome back, Rohan 👋
          </p>
        </div>

        {/* Right */}
        <div className="flex items-center gap-4">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />

            <Input
              placeholder="Search documents..."
              className="w-72 rounded-xl pl-10"
            />
          </div>

          {/* Date */}
          <Button
            variant="outline"
            className="rounded-xl"
          >
            <CalendarDays className="mr-2 h-4 w-4" />
            Today
          </Button>

          {/* Theme Toggle */}
          <ThemeToggle />

          {/* Notification */}
          <Button
            variant="ghost"
            size="icon"
            className="relative rounded-xl"
          >
            <Bell className="h-5 w-5" />

            <span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-red-500" />
          </Button>

          {/* Avatar */}
          <Avatar className="h-11 w-11">
            <AvatarFallback className="bg-primary text-primary-foreground">
              RB
            </AvatarFallback>
          </Avatar>
        </div>
      </div>
    </header>
  );
}