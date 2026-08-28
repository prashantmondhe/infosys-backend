import PageHeader from "@/components/common/PageHeader";
import ActivityLogFilters from "@/components/activity-logs/ActivityLogFilters";
import ActivityLogsTable from "@/components/activity-logs/ActivityLogsTable";
import AnimatedContainer from "@/components/common/AnimatedContainer";

export default function ActivityLogsPage() {
  return (
    <AnimatedContainer>
    <div className="space-y-8">

      <PageHeader
        title="Activity Logs"
        description="Monitor user actions and system activity."
      />

      <ActivityLogFilters />

      <ActivityLogsTable />

    </div>
  </AnimatedContainer>
  );
}