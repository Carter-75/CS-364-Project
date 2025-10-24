const { useEffect, useState } = React;

function App() {
  const [apiStatus, setApiStatus] = useState('checking...');
  const [dbStatus, setDbStatus] = useState('checking...');

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/health')
      .then((r) => r.json())
      .then((data) => setApiStatus(data.status || 'unknown'))
      .catch(() => setApiStatus('unreachable'));

    fetch('http://127.0.0.1:5000/api/db/ping')
      .then((r) => r.json())
      .then((data) => setDbStatus(data.status || 'unknown'))
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

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);