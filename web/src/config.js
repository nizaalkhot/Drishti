// Central API Configuration for Drishti Frontend
// Defaults to port 8001 where Drishti Core runs when 8000 is occupied, or auto-detects 8000.
export const API_BASE = (typeof window !== 'undefined' && window.__DRISHTI_API_BASE__) 
  ? window.__DRISHTI_API_BASE__ 
  : 'http://localhost:8001';
