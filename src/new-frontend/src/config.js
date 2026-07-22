// Single source of truth for backend URLs — see CHANGELOG.md "Notes for
// next-sprint owner" (Sprint 5): these used to be hardcoded separately in
// every page file and had drifted out of sync.
export const API_URL = process.env.REACT_APP_API_URL || 'https://team-24.onrender.com';
export const API_UPLOAD_URL =
  process.env.REACT_APP_UPLOAD_URL || 'https://team-24-1.onrender.com/upload-menu';
