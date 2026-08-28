"use client";

import { useEffect, useState } from "react";

import {
  FileText,
  Download,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

import { getDocuments } from "@/lib/api/api";

type Document = {
  id: number;
  title: string;
  file_name: string;
  file_path: string;
  department: string;
  created_at: string;
};

export default function RecentDocuments() {
  const [documents, setDocuments] = useState<Document[]>([]);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const data = await getDocuments();

      // Show latest 4 documents
      setDocuments(data.slice(0, 4));
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Card className="rounded-2xl border-0 shadow-sm p-6">
      <div className="mb-6 flex items-center justify-between">
        <h2 className="text-xl font-semibold">Recent Documents</h2>

        <Button variant="outline">
          View All
        </Button>
      </div>

      <div className="space-y-4">
        {documents.map((doc) => (
          <div
            key={doc.id}
            className="flex items-center justify-between rounded-xl border p-4 transition hover:bg-slate-50"
          >
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-violet-100">
                <FileText className="text-violet-600" />
              </div>

              <div>
                <h3 className="font-medium">{doc.title}</h3>

                <p className="text-sm text-slate-500">
                  {doc.department} •{" "}
                  {new Date(doc.created_at).toLocaleDateString()}
                </p>
              </div>
            </div>

            {/* Download Button */}
            <a
              href={`http://127.0.0.1:8000/${doc.file_path}`}
              download={doc.file_name}
              target="_blank"
              rel="noopener noreferrer"
            >
              <Button
                size="icon"
                variant="ghost"
              >
                <Download className="h-4 w-4" />
              </Button>
            </a>
          </div>
        ))}
      </div>
    </Card>
  );
}