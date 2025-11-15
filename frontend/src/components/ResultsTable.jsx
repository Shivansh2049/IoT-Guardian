export default function ResultsTable({ results }) {
  if (!results || results.length === 0)
    return <div className="text-black p-4">No scan results.</div>;

  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse">
        <thead>
          <tr className="text-left text-sm text-gray-700">
            <th className="p-3">IP</th>
            <th className="p-3">MAC</th>
            <th className="p-3">Vendor</th>
            <th className="p-3">Open Ports</th>
            <th className="p-3">Risk</th>
            <th className="p-3">Recommendation</th>
          </tr>
        </thead>

        <tbody>
          {results.map((r) => (
            <tr key={r.ip} className="table-row">
              <td className="p-3">{r.ip}</td>
              <td className="p-3">{r.mac}</td>
              <td className="p-3">{r.vendor}</td>

              <td className="p-3">
                {Array.isArray(r.open_ports) && r.open_ports.length > 0 ? (
                  r.open_ports.map((p) => (
                    <div key={p.port ?? p}>
                      {p.port ?? p} {p.service ? `(${p.service})` : ""}
                    </div>
                  ))
                ) : (
                  <span>—</span>
                )}
              </td>

              <td className="p-3 font-bold">{r.risk}</td>
              <td className="p-3">{r.recommendation}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
