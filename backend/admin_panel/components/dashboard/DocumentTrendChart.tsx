"use client";

import { useEffect, useState } from "react";

import {
  LineChart,
  Line,
  ResponsiveContainer,
  CartesianGrid,
  XAxis,
  Tooltip,
} from "recharts";

import { getDocumentTrend } from "@/lib/api/api";

type TrendData = {
  month: string;
  documents: number;
};

export default function DocumentTrendChart() {
  const [data, setData] = useState<TrendData[]>([]);

  useEffect(() => {
    loadTrend();
  }, []);

  const loadTrend = async () => {
    try {
      const trend = await getDocumentTrend();
      setData(trend);
    } catch (error) {
      console.error("Failed to load document trend:", error);
    }
  };

  return (
    <ResponsiveContainer width="100%" height={320}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />

        <XAxis dataKey="month" />

        <Tooltip />

        <Line
          type="monotone"
          dataKey="documents"
          stroke="#7c3aed"
          strokeWidth={4}
          dot={{ r: 5 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}