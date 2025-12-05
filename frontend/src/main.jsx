import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css'; // Import global styles
import App from './App.jsx';

const container = document.getElementById('root');
const root = createRoot(container);
root.render(<App />);


