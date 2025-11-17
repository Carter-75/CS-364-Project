import { useEffect, useState } from 'react';

export default function App() {
  const [apiStatus, setApiStatus] = useState('checking...');
  const [dbStatus, setDbStatus] = useState('checking...');
  const [formData, setFormData] = useState({
    firstname: '',
    lastname: '',
    profilename: '',
    mediatype: '',
    medianame: '',
    description: '',
    releaseyear: '',
    genre: '',
    rating: '',
    ratingtext: '',
    status: '',
    platform: '',
  });
  const [result, setResult] = useState('');
  const [items, setItems] = useState([]);
  const [queryResult, setQueryResult] = useState({
    title: '',
    loading: false,
    data: null,
    error: '',
  });

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

  async function runQuery(endpoint, title) {
    setQueryResult({ title, loading: true, data: null, error: '' });
    try {
      const res = await fetch(endpoint);
      let data = null;
      try {
        data = await res.json();
      } catch (_) {
        // ignore JSON parse errors
      }
      if (!res.ok) {
        const message = (data && (data.error || data.message)) || 'Request failed';
        setQueryResult({ title, loading: false, data: null, error: message });
        return;
      }
      setQueryResult({ title, loading: false, data: data ?? null, error: '' });
    } catch (e) {
      setQueryResult({ title, loading: false, data: null, error: 'Network error' });
    }
  }

  return (
    <div>
    {/*  <h2>Backend Status</h2>
      <ul>
        <li>API: {apiStatus}</li>
        <li>Database: {dbStatus}</li>
      </ul> */}

      <h1>Add your media entry</h1>
      <form
        onSubmit={async (e) => {
          e.preventDefault();
          try {
            const payload = {
              ...formData,
              releaseyear: formData.releaseyear ? Number(formData.releaseyear) : null,
              rating: formData.rating ? Number(formData.rating) : null,
            };
            const response = await fetch('/api/media-entries', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(payload),
            });
            let responseData = null;
            try {
              responseData = await response.json();
            } catch (_) {
              // ignore JSON parse errors; may be empty body
            }

            if (response.ok || (responseData && (responseData.status === 'ok' || responseData.success))) {
              setResult('SAVED!');
              setFormData({
                firstname: '',
                lastname: '',
                profilename: '',
                mediatype: '',
                medianame: '',
                description: '',
                releaseyear: '',
                genre: '',
                rating: '',
                ratingtext: '',
                status: '',
                platform: '',
              });
            } else {
              const serverError = responseData?.error || responseData?.message;
              setResult(serverError ? `Insert FAILED: ${serverError}` : 'Insert FAILED');
            }
          } catch (err) {
              setResult('Network error');
          }
        }}
      >
        <label htmlFor="firstname">First name</label>
        <input
          id="firstname"
          type="text"
          value={formData.firstname}
          onChange={(e) => setFormData((p) => ({ ...p, firstname: e.target.value }))}
          required
        />

        <label htmlFor="lastname">Last name</label>
        <input
          id="lastname"
          type="text"
          value={formData.lastname}
          onChange={(e) => setFormData((p) => ({ ...p, lastname: e.target.value }))}
          required
        />

        <label htmlFor="profilename">Profile name</label>
        <input
          id="profilename"
          type="text"
          value={formData.profilename}
          onChange={(e) => setFormData((p) => ({ ...p, profilename: e.target.value }))}
          required
        />

        <label htmlFor="mediatype">Media type</label>
        <input
          id="mediatype"
          type="text"
          value={formData.mediatype}
          onChange={(e) => setFormData((p) => ({ ...p, mediatype: e.target.value }))}
          required
        />

        <label htmlFor="medianame">Media name</label>
        <input
          id="medianame"
          type="text"
          value={formData.medianame}
          onChange={(e) => setFormData((p) => ({ ...p, medianame: e.target.value }))}
          required
        />

        <label htmlFor="description">Description (optional)</label>
        <textarea
          id="description"
          value={formData.description}
          onChange={(e) => setFormData((p) => ({ ...p, description: e.target.value }))}
          rows={3}
        />

        <label htmlFor="releaseyear">Release year</label>
        <input
          id="releaseyear"
          type="number"
          value={formData.releaseyear}
          onChange={(e) => setFormData((p) => ({ ...p, releaseyear: e.target.value }))}
          required
        />

        <label htmlFor="genre">Genre</label>
        <input
          id="genre"
          type="text"
          value={formData.genre}
          onChange={(e) => setFormData((p) => ({ ...p, genre: e.target.value }))}
          required
        />

        <label htmlFor="rating">Rating (1–5)</label>
        <input
          id="rating"
          type="number"
          min={1}
          max={5}
          step={1}
          value={formData.rating}
          onChange={(e) => setFormData((p) => ({ ...p, rating: e.target.value }))}
          required
        />

        <label htmlFor="ratingtext">Rating text (optional)</label>
        <input
          id="ratingtext"
          type="text"
          value={formData.ratingtext}
          onChange={(e) => setFormData((p) => ({ ...p, ratingtext: e.target.value }))}
        />

        <label htmlFor="status">Status</label>
        <input
          id="status"
          type="text"
          value={formData.status}
          onChange={(e) => setFormData((p) => ({ ...p, status: e.target.value }))}
          required
        />

        <label htmlFor="platform">Platform</label>
        <input
          id="platform"
          type="text"
          value={formData.platform}
          onChange={(e) => setFormData((p) => ({ ...p, platform: e.target.value }))}
          required
        />
        <button type="submit">SAVE</button>
      </form>
      {result && <p aria-live='polite'>{result}</p>}

      <hr />
      <section aria-labelledby="queries-title">
        <h2 id="queries-title">Advanced Queries</h2>
        <div>
          <button
            type="button"
            onClick={() =>
              runQuery('/api/queries/top-rated-by-type', 'Top 5 highest-rated media by type')
            }
          >
            Top rated by type
          </button>
          <button
            type="button"
            onClick={() =>
              runQuery(
                '/api/queries/top-users-completed',
                'Top 5 users who completed the most media'
              )
            }
          >
            Top users completed
          </button>
          <button
            type="button"
            onClick={() =>
              runQuery(
                '/api/queries/top-media-completions',
                'Top 5 media with the most completions'
              )
            }
          >
            Top media completions
          </button>
          <button
            type="button"
            onClick={() =>
              runQuery('/api/queries/avg-rating-by-genre', 'Average rating per genre')
            }
          >
            Avg rating by genre
          </button>
          <button
            type="button"
            onClick={() =>
              runQuery(
                '/api/queries/users-rated-high',
                'Users who rated at least one media high'
              )
            }
          >
            Users rated high
          </button>
          <button
            type="button"
            onClick={() =>
              runQuery(
                '/api/queries/recent-low-rated',
                '10 most recent low-rated media (≤ 3)'
              )
            }
          >
            Recent low-rated media
          </button>
        </div>
        {queryResult.loading && <p>Loading…</p>}
        {queryResult.error && (
          <p role="alert">Query failed: {queryResult.error}</p>
        )}
        {queryResult.data && (
          <div>
            <h3>{queryResult.title}</h3>
            <pre>{JSON.stringify(queryResult.data, null, 2)}</pre>
          </div>
        )}
      </section>

      {/*<h2>Recent names</h2>
      <ul>
        {items.map((it) => (
          <li key={it.id}>
            {it.name} — {it.created_at ? new Date(it.created_at).toLocaleString() : ''}
          </li>
        ))}
      </ul>*/}
    </div>
  );
}

