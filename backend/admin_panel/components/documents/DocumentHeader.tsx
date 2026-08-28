import UploadDocumentModal from "./UploadDocumentModal";

export default function DocumentHeader() {
  return (
    <div className="flex items-center justify-between">

      <div>

        <h1 className="text-3xl font-bold">
          Documents
        </h1>

        <p className="mt-2 text-slate-500">
          Upload and manage enterprise documents.
        </p>

      </div>

      <UploadDocumentModal />

    </div>
  );
}