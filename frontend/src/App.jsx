import { useEffect, useState } from 'react';

export default function App() {
  const [apiStatus, setApiStatus] = useState('checking...');
  const [dbStatus, setDbStatus] = useState('checking...');

  useEffect(() => {
    fetch('/api/health')
      .then((r) => r.json())
      .then((d) => setApiStatus(d.status || 'unknown'))
      .catch(() => setApiStatus('unreachable'));

    fetch('/api/db/ping')
      .then((r) => r.json())
      .then((d) => setDbStatus(d.status || 'unknown'))
      .catch(() => setDbStatus('unreachable'));
  }, []);

  return (
    <div>
      <h2>Backend Status</h2>
      <ul>
        <li>API: {apiStatus}</li>
        <li>Database: {dbStatus}</li>
      </ul>
    </div>
  );
}

