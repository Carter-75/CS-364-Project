import React from 'react';

export default function QueryResults({ title, data, loading, error }) {
  if (loading) {
    return <div className="loading-spinner">Loading data...</div>;
  }

  if (error) {
    return <div className="error-message">Error: {error}</div>;
  }

  if (!data) {
    return null;
  }

  // If data is an array, show a table
  if (Array.isArray(data) && data.length > 0) {
    const headers = Object.keys(data[0]);

    return (
      <div className="results-container">
        <h3>{title}</h3>
        <table>
          <thead>
            <tr>
              {headers.map((header) => (
                <th key={header}>{header.replace(/_/g, ' ')}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, index) => (
              <tr key={index}>
                {headers.map((header) => (
                  <td key={`${index}-${header}`}>
                    {typeof row[header] === 'object' && row[header] !== null
                      ? JSON.stringify(row[header])
                      : String(row[header])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        <p style={{ textAlign: 'right', fontSize: '0.8rem', color: '#666', marginTop: '1rem' }}>
          {data.length} results found
        </p>
      </div>
    );
  }

  // If data is empty array
  if (Array.isArray(data) && data.length === 0) {
    return (
      <div className="results-container">
        <h3>{title}</h3>
        <p>No results found.</p>
      </div>
    );
  }

  // Fallback for non-array data (single object or message)
  return (
    <div className="results-container">
      <h3>{title}</h3>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
