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

