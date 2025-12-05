import React, { useState } from 'react';
import QueryResults from './QueryResults';

export default function SearchSection() {
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('media');
  const [sort, setSort] = useState('az');
  const [results, setResults] = useState({
    loading: false,
    data: null,
    error: ''
  });

  const handleSearch = async (e) => {
    e.preventDefault();
    setResults({ loading: true, data: null, error: '' });

    try {
      const params = new URLSearchParams({ q: query, category, sort });
      const res = await fetch(`/api/search?${params}`);
      const data = await res.json();

      if (!res.ok) {
        setResults({ loading: false, data: null, error: data.error || 'Search failed' });
      } else {
        setResults({ loading: false, data: data, error: '' });
      }
    } catch (err) {
      setResults({ loading: false, data: null, error: 'Network error' });
    }
  };

  return (
    <div className="search-nav-container">
      <form onSubmit={handleSearch} className="search-nav-form">
        <input
          type="text"
          placeholder="Search..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="search-input"
        />
        
        <select 
          value={category} 
          onChange={(e) => {
            setCategory(e.target.value);
            setSort('az');
          }}
          className="search-select"
        >
          <option value="media">Media</option>
          <option value="user">User</option>
          <option value="genre">Genre</option>
        </select>

        <select 
          value={sort} 
          onChange={(e) => setSort(e.target.value)}
          className="search-select"
        >
          <option value="az">A-Z</option>
          <option value="za">Z-A</option>
          
          {category === 'media' && (
            <>
              <option value="rating_desc">Highest Rated</option>
              <option value="rating_asc">Lowest Rated</option>
              <option value="year_desc">Newest</option>
              <option value="year_asc">Oldest</option>
            </>
          )}
          
          {category === 'user' && (
            <>
              <option value="count_desc">Most Reviews</option>
              <option value="count_asc">Least Reviews</option>
            </>
          )}

          {category === 'genre' && (
            <>
              <option value="count_desc">Most Media</option>
              <option value="count_asc">Least Media</option>
              <option value="rating_desc">Highest Avg Rating</option>
              <option value="rating_asc">Lowest Avg Rating</option>
            </>
          )}
        </select>

        <button type="submit" className="search-button">Go</button>
      </form>

      {(results.data || results.error) && (
        <div className="search-results-dropdown">
          <div className="results-header-bar">
            <span>{results.error ? 'Error' : `Results: ${results.data ? results.data.length : 0}`}</span>
            <button 
              type="button" 
              className="close-results-btn"
              onClick={() => setResults({ ...results, data: null, error: '' })}
            >
              ×
            </button>
          </div>
          <QueryResults 
            title=""
            data={results.data}
            loading={results.loading}
            error={results.error}
          />
        </div>
      )}
    </div>
  );
}
