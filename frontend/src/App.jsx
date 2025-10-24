import { useEffect, useState } from 'react';

export default function App() {
  const [apiStatus, setApiStatus] = useState('checking...');
  const [dbStatus, setDbStatus] = useState('checking...');
  const [inputName, setInputName] = useState('');
  const [result, setResult] = useState('');

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
    {/*  <h2>Backend Status</h2>
      <ul>
        <li>API: {apiStatus}</li>
        <li>Database: {dbStatus}</li>
      </ul> */}

      <h1>Add your name!</h1>
      <form
        onSubmit={async (e) => {
          e.preventDefault();
          const name = inputName.trim();
          if (!name) return;
          try {
            const res = await fetch('/api/names', {
              method: "POST",
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({name}),
            });
            /*const data = await res.json();
            if (data.status === "ok") {
              setResult("SAVED!");
              setInputName('');
            } else {
              setResult(data.error || 'Insert FAILED');
            }*/
          } catch (err) {
              setResult('Network error');
          }
        }}
      >
        <label htmlFor ="app-name">What is your name?</label>
        <input id="app-name" type="text" value={inputName} onChange={(e) => setInputName(e.target.value)} required/>
        <button type="submit">SAVE</button>
      </form>
      {result && <p aria-live='polite'>{result}</p>}
    </div>
  );
}

