export default function SummaryCards({ results }) {
  const avg = results.length
    ? (results.reduce((s, r) => s + (r.risk || 0), 0) / results.length).toFixed(1)
    : '—';

  return (
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 my-4">
      <div className="p-3 bg-white/90 rounded">
        <div className="text-sm text-gray-600">Devices Found</div>
        <div className="text-2xl font-bold">{results.length}</div>
      </div>

      <div className="p-3 bg-white/90 rounded">
        <div className="text-sm text-gray-600">Average Risk</div>
        <div className="text-2xl font-bold">{avg}</div>
      </div>

      <div className="p-3 bg-white/90 rounded">
        <div className="text-sm text-gray-600">High Risk (&gt;7)</div>
        <div className="text-2xl font-bold text-red-600">
          {results.filter((r) => r.risk > 7).length}
        </div>
      </div>
    </div>
  );
}
