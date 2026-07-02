import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

const MAX_FILE_SIZE = 8 * 1024 * 1024;
const API_UPLOAD_URL = 'https://team-24-1.onrender.com/upload-menu';

function UploadMenu() {
  const navigate = useNavigate();
  const [budget, setBudget] = useState('');
  const [budgetError, setBudgetError] = useState('');
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [fileName, setFileName] = useState('');
  const [fileSize, setFileSize] = useState('');
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [mood, setMood] = useState('');

  const fileInputRef = useRef(null);

  const handleBudgetChange = (e) => {
    const value = e.target.value;
    setBudgetError('');
    if (value === '' || /^\d*\.?\d*$/.test(value)) {
      setBudget(value);
      if (value !== '' && parseFloat(value) <= 0) {
        setBudgetError('Budget must be greater than 0');
      }
    }
  };

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0];
    setError('');
    setSuccess('');
    if (!selectedFile) return;

    if (!['image/jpeg', 'image/png'].includes(selectedFile.type)) {
      setError('Invalid format. Please upload JPEG or PNG.');
      fileInputRef.current.value = '';
      return;
    }
    if (selectedFile.size > MAX_FILE_SIZE) {
      setError(`File too large. Max 8 MB. Your file: ${(selectedFile.size / 1024 / 1024).toFixed(2)} MB`);
      fileInputRef.current.value = '';
      return;
    }

    const reader = new FileReader();
    reader.onload = (event) => {
      setPreview(event.target.result);
      setFile(selectedFile);
      setFileName(selectedFile.name);
      setFileSize((selectedFile.size / 1024 / 1024).toFixed(2));
    };
    reader.readAsDataURL(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a photo first.');
      return;
    }
    if (budgetError) return;

    sessionStorage.setItem('orderly_mood', mood);
    setUploading(true);
    setError('');
    setSuccess('');

    if (budget) {
      localStorage.setItem('orderly_budget', budget);
    } else {
      localStorage.removeItem('orderly_budget');
    }

    try {
      const formData = new FormData();
      formData.append('photo', file);

      const response = await fetch(API_UPLOAD_URL, { method: 'POST', body: formData });

      if (!response.ok) {
        let errorMsg = 'Upload failed';
        try { const errData = await response.json(); errorMsg = errData.error || errData.detail || errorMsg; } catch {}
        throw new Error(errorMsg);
      }

      const data = await response.json();
      if (data.menu && data.menu.length > 0) {
        localStorage.setItem('orderly_menu', JSON.stringify(data.menu));
      } else {
        localStorage.removeItem('orderly_menu');
      }

      setSuccess('Menu uploaded! Getting your recommendation...');
      setTimeout(() => navigate('/food-recommender'), 1200);
    } catch (err) {
      const msg = err.message || 'Upload failed';
      setError(msg + ' — you can skip the photo and use the default menu instead.');
    } finally {
      setUploading(false);
    }
  };

  const handleRemove = () => {
    setFile(null);
    setPreview(null);
    setFileName('');
    setFileSize('');
    setSuccess('');
    setError('');
    fileInputRef.current.value = '';
    localStorage.removeItem('orderly_menu');
  };

  const handleSkipPhoto = () => {
    if (budget) localStorage.setItem('orderly_budget', budget);
    else localStorage.removeItem('orderly_budget');
    localStorage.removeItem('orderly_menu');
    sessionStorage.setItem('orderly_mood', mood);
    navigate('/food-recommender');
  };

  return (
    <div className="upload-page">
      <div className="upload-container">
        <h2>Budget & Menu Photo</h2>
        <p className="subtitle">Step 2 of 3 — Set your budget and upload a menu photo</p>

        <div className="upload-box">
          <div className="form-group" style={{ textAlign: 'left', marginBottom: 24 }}>
            <label className="form-label">
              Max Budget <span className="optional">(optional)</span>
            </label>
            <p className="hint">We'll only recommend dishes within your budget</p>
            <div className="budget-input-wrapper" style={{ position: 'relative', display: 'inline-block' }}>
              <input
                type="text"
                placeholder="e.g. 15"
                value={budget}
                onChange={handleBudgetChange}
                className={`form-input budget-input ${budgetError ? 'input-error' : ''}`}
                style={{ padding: '10px 36px 10px 12px', border: '2px solid #e2e8f0', borderRadius: 8, fontSize: 16, width: 160 }}
              />
              <span style={{ position: 'absolute', right: 12, top: '50%', transform: 'translateY(-50%)', color: '#718096' }}>$</span>
            </div>
            {budgetError && <p className="error-message" style={{ color: '#e53e3e', fontSize: 13, marginTop: 4 }}>{budgetError}</p>}
          </div>

          <div className="form-group" style={{ textAlign: 'left', marginBottom: 24 }}>
            <label className="form-label">
              What are you in the mood for today? <span className="optional">(optional)</span>
            </label>
            <p className="hint">e.g. something light, warm soup, pasta...</p>
            <input
              type="text"
              className="form-select"
              placeholder="e.g. something light, warm soup, pasta..."
              value={mood}
              onChange={(e) => setMood(e.target.value)}
            />
          </div>

          <input
            type="file"
            ref={fileInputRef}
            accept="image/jpeg,image/png"
            onChange={handleFileSelect}
            style={{ display: 'none' }}
          />

          <button className="upload-btn" onClick={() => fileInputRef.current.click()}>
            {preview ? 'Choose another photo' : 'Choose Menu Photo'}
          </button>
          <p className="hint">Supported: JPEG, PNG • Max 8 MB</p>

          {preview && (
            <div className="photo-preview">
              <img src={preview} alt="Menu preview" />
              <p className="file-info">{fileName} ({fileSize} MB)</p>
              <div className="actions">
                <button className="submit-btn" onClick={handleUpload} disabled={uploading}>
                  {uploading ? 'Uploading...' : 'Send for processing'}
                </button>
                <button className="remove-btn" onClick={handleRemove}>Remove</button>
              </div>
            </div>
          )}

          {error && <div className="message error">{error}</div>}
          {success && <div className="message info">{success}</div>}

          <button
            onClick={handleSkipPhoto}
            style={{ marginTop: 20, background: 'transparent', border: '1px dashed #a0aec0', padding: '10px 24px', borderRadius: 8, color: '#718096', cursor: 'pointer', fontSize: 15 }}
          >
            Skip photo — use default menu →
          </button>
        </div>
      </div>
    </div>
  );
}

export default UploadMenu;