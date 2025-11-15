import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

export default function RiskChart({ results }) {
  if (!results || results.length === 0) return null;

  return (
    <div className="mb-4">
      <h3 className="text-lg font-semibold mb-2">Risk Distribution</h3>
      <div style={{ width: "100%", height: 260 }}>
        <ResponsiveContainer>
          <BarChart data={results}>
            <XAxis dataKey="ip" stroke="#111" />
            <YAxis stroke="#111" />
            <Tooltip />
            <Bar dataKey="risk" fill="#4cc9ff" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
