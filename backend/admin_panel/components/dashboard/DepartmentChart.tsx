"use client";

import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
} from "recharts";

const data = [
  { name: "HR", value: 25 },
  { name: "Sales", value: 20 },
  { name: "Finance", value: 18 },
  { name: "IT", value: 22 },
  { name: "Legal", value: 15 },
];

const COLORS = [
  "#7c3aed",
  "#8b5cf6",
  "#a78bfa",
  "#c4b5fd",
  "#ddd6fe",
];

export default function DepartmentChart() {
  return (
    <ResponsiveContainer width="100%" height={320}>
      <PieChart>
        <Pie
          data={data}
          innerRadius={65}
          outerRadius={95}
          dataKey="value"
        >
          {data.map((_, index) => (
            <Cell
              key={index}
              fill={COLORS[index]}
            />
          ))}
        </Pie>

      </PieChart>
    </ResponsiveContainer>
  );
}