// Central API Configuration for Drishti Frontend
export const API_BASE = (typeof window !== 'undefined' && window.__DRISHTI_API_BASE__) 
  ? window.__DRISHTI_API_BASE__ 
  : (import.meta.env.VITE_API_BASE !== undefined
      ? import.meta.env.VITE_API_BASE
      : (typeof window !== 'undefined' && window.location.port !== '5173' ? '' : 'http://localhost:8000'));
