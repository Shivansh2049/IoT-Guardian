import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Header from './components/Header';
import ScanControls from './components/ScanControls';
import SummaryCards from './components/SummaryCards';
import RiskChart from './components/RiskChart';
import ResultsTable from './components/ResultsTable';

export default function App() {
  const [network, setNetwork] = useState('192.168.1.0/24');
  const [profile, setProfile] = useState('fast');
  const [scanId, setScanId] = useState(null);
  const [status, setStatus] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const startScan = async () => {
    setLoading(true);
    setResults([]);
    try {
      const res = await axios.post('/api/scan/start', { network, profile });
      setScanId(res.data.scan_id);
      setStatus('started');
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to start scan');
    }
    setLoading(false);
  };

  useEffect(() => {
    if (!scanId) return;

    let done = false;

    const check = async () => {
      try {
        const s = await axios.get(`/api/scan/status/${scanId}`);
        setStatus(s.data.status);

        if (s.data.status === 'finished') {
          const r = await axios.get(`/api/scan/result/${scanId}`);
          const data = r.data.results || r.data.devices || [];
          setResults(data);
          done = true;
        }
      } catch (e) {}
    };

    const interval = setInterval(() => {
      if (!done) check();
    }, 3000);

    check();
    return () => clearInterval(interval);
  }, [scanId]);

  return (
    <div className="p-6">
      <Header />

      <div className="mt-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="card">
            <ScanControls
              network={network}
              setNetwork={setNetwork}
              profile={profile}
              setProfile={setProfile}
              startScan={startScan}
              loading={loading}
              status={status}
            />

            <SummaryCards results={results} />
            <RiskChart results={results} />
          </div>
        </div>

        <div>
          <div className="card">
            <h3 className="text-xl font-semibold mb-3">Quick Actions</h3>
            <button
              className="px-4 py-2 rounded bg-[var(--accent)] font-bold text-black"
              onClick={() => {
                navigator.clipboard.writeText(scanId || '');
                alert('Copied Scan ID');
              }}
            >
              Copy Scan ID
            </button>

            <p className="text-sm mt-3 text-gray-700">
              Status: <strong>{status || 'idle'}</strong>
            </p>
          </div>
        </div>
      </div>

      <div className="mt-6 card">
        <ResultsTable results={results} />
      </div>
    </div>
  );
}

