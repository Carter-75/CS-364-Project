import { useEffect, useState } from 'react';
import QueryResults from './components/QueryResults';

export default function App() {
  // Updated by Copilot
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

  const commonMediaTypes = ['Movie', 'Show', 'Song', 'Book', 'Game'];
  const commonGenres = ['Action', 'Comedy', 'Sci-Fi', 'Horror', 'Romance', 'Thriller', 'Drama', 'Fantasy', 'Documentary', 'Animation'];
  const commonPlatforms = ['Netflix', 'Hulu', 'Disney+', 'HBO Max', 'Spotify', 'YouTube', 'Amazon Prime', 'Apple TV', 'Steam', 'PlayStation', 'Xbox'];

  const [isCustomMediaType, setIsCustomMediaType] = useState(false);
  const [isCustomGenre, setIsCustomGenre] = useState(false);
  const [isCustomPlatform, setIsCustomPlatform] = useState(false);
  const [isCustomYear, setIsCustomYear] = useState(false);

  const currentYear = new Date().getFullYear();
  // 1888 is often cited as the year of the first motion picture (Roundhay Garden Scene).
  // Books go back much further, but for a dropdown, 1800 is a reasonable cutoff for "modern" media.
  // Older items can use the "Custom" option.
  const years = [];
  for (let y = currentYear + 1; y >= 1800; y--) {
    years.push(y);
  }

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
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>MediaWatchList</h1>
        <div className="status-panel">
          <div className="status-items">
            <div className="status-item">
              <span className="label">API:</span>
              <span className={`value ${apiStatus === 'ok' ? 'ok' : 'error'}`}>{apiStatus}</span>
            </div>
            <div className="status-item">
              <span className="label">Database:</span>
              <span className={`value ${dbStatus === 'ok' ? 'ok' : 'error'}`}>{dbStatus}</span>
            </div>
          </div>
        </div>
      </header>

      <div className="dashboard-content">
        <section className="form-section">
          <h2>Add Entry</h2>
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
              setIsCustomMediaType(false);
              setIsCustomGenre(false);
              setIsCustomPlatform(false);
              setIsCustomYear(false);
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
        <select
          id="mediatype-select"
          value={isCustomMediaType ? 'custom' : formData.mediatype}
          onChange={(e) => {
            if (e.target.value === 'custom') {
              setIsCustomMediaType(true);
              setFormData((p) => ({ ...p, mediatype: '' }));
            } else {
              setIsCustomMediaType(false);
              setFormData((p) => ({ ...p, mediatype: e.target.value }));
            }
          }}
          required={!isCustomMediaType}
        >
          <option value="" disabled>Select media type</option>
          {commonMediaTypes.map((t) => (
            <option key={t} value={t}>{t}</option>
          ))}
          <option value="custom">Enter custom...</option>
        </select>
        {isCustomMediaType && (
          <input
            id="mediatype"
            type="text"
            placeholder="Enter custom media type"
            value={formData.mediatype}
            onChange={(e) => setFormData((p) => ({ ...p, mediatype: e.target.value }))}
            required
          />
        )}

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
        <select
          id="releaseyear-select"
          value={isCustomYear ? 'custom' : formData.releaseyear}
          onChange={(e) => {
            if (e.target.value === 'custom') {
              setIsCustomYear(true);
              setFormData((p) => ({ ...p, releaseyear: '' }));
            } else {
              setIsCustomYear(false);
              setFormData((p) => ({ ...p, releaseyear: e.target.value }));
            }
          }}
          required={!isCustomYear}
        >
          <option value="" disabled>Select year</option>
          <option value="custom">Enter custom...</option>
          {years.map((y) => (
            <option key={y} value={y}>{y}</option>
          ))}
        </select>
        {isCustomYear && (
          <input
            id="releaseyear"
            type="number"
            placeholder="Enter custom year"
            value={formData.releaseyear}
            onChange={(e) => setFormData((p) => ({ ...p, releaseyear: e.target.value }))}
            required
          />
        )}

        <label htmlFor="genre">Genre</label>
        <select
          id="genre-select"
          value={isCustomGenre ? 'custom' : formData.genre}
          onChange={(e) => {
            if (e.target.value === 'custom') {
              setIsCustomGenre(true);
              setFormData((p) => ({ ...p, genre: '' }));
            } else {
              setIsCustomGenre(false);
              setFormData((p) => ({ ...p, genre: e.target.value }));
            }
          }}
          required={!isCustomGenre}
        >
          <option value="" disabled>Select genre</option>
          {commonGenres.map((g) => (
            <option key={g} value={g}>{g}</option>
          ))}
          <option value="custom">Enter custom...</option>
        </select>
        {isCustomGenre && (
          <input
            id="genre"
            type="text"
            placeholder="Enter custom genre"
            value={formData.genre}
            onChange={(e) => setFormData((p) => ({ ...p, genre: e.target.value }))}
            required
          />
        )}

        <label htmlFor="rating">Rating (1–5)</label>
        <select
          id="rating"
          value={formData.rating}
          onChange={(e) => setFormData((p) => ({ ...p, rating: e.target.value }))}
          required
        >
          <option value="" disabled>Select rating</option>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
        </select>

        <label htmlFor="ratingtext">Rating text (optional)</label>
        <input
          id="ratingtext"
          type="text"
          value={formData.ratingtext}
          onChange={(e) => setFormData((p) => ({ ...p, ratingtext: e.target.value }))}
        />

        <label htmlFor="status">Status</label>
        <select
          id="status"
          value={formData.status}
          onChange={(e) => setFormData((p) => ({ ...p, status: e.target.value }))}
          required
        >
          <option value="" disabled>Select status</option>
          <option value="Planning">Planning</option>
          <option value="Watching">Watching</option>
          <option value="Completed">Completed</option>
          <option value="Havent Watched">Havent Watched</option>
        </select>

        <label htmlFor="platform">Platform</label>
        <select
          id="platform-select"
          value={isCustomPlatform ? 'custom' : formData.platform}
          onChange={(e) => {
            if (e.target.value === 'custom') {
              setIsCustomPlatform(true);
              setFormData((p) => ({ ...p, platform: '' }));
            } else {
              setIsCustomPlatform(false);
              setFormData((p) => ({ ...p, platform: e.target.value }));
            }
          }}
          required={!isCustomPlatform}
        >
          <option value="" disabled>Select platform</option>
          {commonPlatforms.map((pl) => (
            <option key={pl} value={pl}>{pl}</option>
          ))}
          <option value="custom">Enter custom...</option>
        </select>
        {isCustomPlatform && (
          <input
            id="platform"
            type="text"
            placeholder="Enter custom platform"
            value={formData.platform}
            onChange={(e) => setFormData((p) => ({ ...p, platform: e.target.value }))}
            required
          />
        )}
        <button type="submit">SAVE</button>
      </form>
      {result && <p aria-live='polite' className="result-message">{result}</p>}
        </section>

        <section className="queries-section" aria-labelledby="queries-title">
        <h2 id="queries-title">Advanced Queries</h2>
        <div className="query-buttons">
          <button
            type="button"
            onClick={() =>
              runQuery('/api/top-rated-media', 'Top 5 highest-rated media by type')
            }
          >
            Top rated by type
          </button>
          <button
            type="button"
            onClick={() =>
              runQuery(
                '/api/top-users-completed',
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
                '/api/top-media-completions',
                'Top 5 media with the most completions'
              )
            }
          >
            Top media completions
          </button>
          <button
            type="button"
            onClick={() =>
              runQuery('/api/avg-rating-genre', 'Average rating per genre')
            }
          >
            Avg rating by genre
          </button>
          <button
            type="button"
            onClick={() =>
              runQuery(
                '/api/users-rated-high',
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
                '/api/low-rated-recent',
                '10 most recent low-rated media (≤ 3)'
              )
            }
          >
            Recent low-rated media
          </button>
        </div>
        
        <QueryResults 
          title={queryResult.title}
          data={queryResult.data}
          loading={queryResult.loading}
          error={queryResult.error}
        />
        </section>
      </div>
    </div>
  );
}

