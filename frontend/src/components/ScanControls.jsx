export default function ScanControls({
  network,
  setNetwork,
  profile,
  setProfile,
  startScan,
  loading,
  status
}) {
  return (
    <div className="mb-4">
      <div className="flex flex-wrap gap-3">
        <input
          value={network}
          onChange={(e) => setNetwork(e.target.value)}
          className="flex-1 p-2 rounded"
        />

        <select
          value={profile}
          onChange={(e) => setProfile(e.target.value)}
          className="p-2 rounded"
        >
          <option value="fast">Fast</option>
          <option value="normal">Normal</option>
          <option value="deep">Deep</option>
        </select>

        <button
          onClick={startScan}
          disabled={loading}
          className="px-4 py-2 rounded bg-[var(--accent)] text-black font-bold"
        >
          {loading ? 'Starting...' : status === 'started' ? 'Scanning...' : 'Start Scan'}
        </button>
      </div>

      <p className="text-sm mt-2 text-gray-700">
        Enter local network (example: 192.168.1.0/24)
      </p>
    </div>
  );
}
