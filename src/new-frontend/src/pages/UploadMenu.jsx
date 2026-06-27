import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

const MAX_FILE_SIZE = 8 * 1024 * 1024;
const API_UPLOAD_URL = 'https://team-24-1.onrender.com/upload-menu';
const RECOMMENDER_ROUTE = '/food-recommender';

function UploadMenu() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [fileName, setFileName] = useState('');
  const [fileSize, setFileSize] = useState('');
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const fileInputRef = useRef(null);

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0];
    setError('');
    setSuccess('');

    if (!selectedFile) return;

    const validTypes = ['image/jpeg', 'image/png'];
    if (!validTypes.includes(selectedFile.type)) {
      setError('Invalid format. Please upload JPEG, PNG.');
      setFile(null);
      setPreview(null);
      setFileName('');
      setFileSize('');
      fileInputRef.current.value = '';
      return;
    }

    if (selectedFile.size > MAX_FILE_SIZE) {
      setError(
        `File too large. Maximum size is 8 MB. Your file: ${(selectedFile.size / 1024 / 1024).toFixed(2)} MB`
      );
      setFile(null);
      setPreview(null);
      setFileName('');
      setFileSize('');
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

    setUploading(true);
    setError('');
    setSuccess('');

    try {
      const formData = new FormData();
      formData.append('photo', file);

      const response = await fetch(API_UPLOAD_URL, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        let errorMsg = 'Upload failed';
        try {
          const errData = await response.json();
          errorMsg = errData.error || errorMsg;
        } catch {}
        throw new Error(errorMsg);
      }

      const data = await response.json();
      if (data.menu && data.menu.length > 0) {
        localStorage.setItem('orderly_menu', JSON.stringify(data.menu));
      }
      setSuccess('Menu uploaded successfully!');
      
    } catch (err) {
      console.error('Upload failed:', err);
      setError(`${err.message || 'Upload failed'}`);
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

  const handleChooseClick = () => {
    fileInputRef.current.click();
  };

  const handleGoToRecommendations = () => {
    navigate(RECOMMENDER_ROUTE);
  };

  return (
    <div className="upload-page">
      <div className="upload-container">
        <h2>Upload Menu Photo</h2>
        <p className="subtitle">Select a photo of the menu from your gallery to upload for processing</p>

        <div className="upload-box">
          <input
            type="file"
            ref={fileInputRef}
            accept="image/jpeg,image/png"
            onChange={handleFileSelect}
            style={{ display: 'none' }}
          />

          <button className="upload-btn" onClick={handleChooseClick}>
            {preview ? 'Choose another photo' : 'Choose Photo'}
          </button>

          <p className="hint">Supported formats: JPEG, PNG • Max size: 8 MB</p>

          {preview && (
            <div className="photo-preview">
              <img src={preview} alt="Menu preview" />
              <p className="file-info"> {fileName} ({fileSize} MB)</p>
              <div className="actions">
                <button
                  className="submit-btn"
                  onClick={handleUpload}
                  disabled={uploading}
                >
                  {uploading ? 'Uploading...' : 'Send for processing'}
                </button>
                <button className="remove-btn" onClick={handleRemove}>
                  Remove
                </button>
              </div>
            </div>
          )}

          {error && <div className="message error">{error}</div>}
          {success && <div className="message info">{success}</div>}

          {preview && success && (
            <button 
              className="recommendations-btn" 
              onClick={handleGoToRecommendations}
              style={{ marginTop: '15px' }}
            >
              Get recommendations →
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default UploadMenu;
