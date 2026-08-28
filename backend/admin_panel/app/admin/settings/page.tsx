import PageHeader from "@/components/common/PageHeader";

import CompanySettings from "@/components/settings/CompanySettings";
import SecuritySettings from "@/components/settings/SecuritySettings";
import NotificationSettings from "@/components/settings/NotificationSettings";
import AppearanceSettings from "@/components/settings/AppearanceSettings";
import AnimatedContainer from "@/components/common/AnimatedContainer";

export default function SettingsPage() {
  return (
    <AnimatedContainer>
      <div className="space-y-8">

        <PageHeader
          title="Settings"
          description="Manage your organization and application preferences."
        />

        <CompanySettings />

        <div className="grid gap-6 lg:grid-cols-2">

          <SecuritySettings />

          <NotificationSettings />

        </div>

        <AppearanceSettings />

      </div>
    </AnimatedContainer>  
  );
}