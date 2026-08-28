import PageHeader from "@/components/common/PageHeader";
import StorageStats from "@/components/storage/StorageStats";
import StorageFilters from "@/components/storage/StorageFilters";
import StorageTable from "@/components/storage/StorageTable";

export default function StoragePage() {
  return (
    <div className="space-y-8">

      <PageHeader
        title="Storage"
        description="Manage uploaded files and monitor storage usage."
      />

      <StorageStats />

      <StorageFilters />

      <StorageTable />

    </div>
  );
}