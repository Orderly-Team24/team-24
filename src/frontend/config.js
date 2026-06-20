// Shared frontend config. Loaded as a regular <script> tag before script.js.
//
// Set API_BASE_URL to the deployed backend origin. Examples:
//   ""                                          → same origin (use only if backend is reverse-proxied)
//   "https://orderly-recommender.onrender.com"  → backend service
//   "https://orderly-upload.onrender.com"       → upload-menu service
//
// Two endpoints, two backends:
//   API_RECOMMENDER  → POST /display/recommendations   (src/backend)
//   API_UPLOAD       → POST /upload-menu               (src/upload-menu-backend)

window.ORDERLY_CONFIG = {
    API_RECOMMENDER: "https://team-24.onrender.com",
    API_UPLOAD:      "https://team-24-1.onrender.com",
};