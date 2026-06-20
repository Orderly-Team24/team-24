// ---- Config ---------------------------------------------------------------
// Point this at the deployed backend. After deploy on Render it will look
// like "https://orderly-upload-menu.onrender.com". Leave empty to use the
// same origin as the page (works when the API is reverse-proxied).
const API_BASE_URL = "";

// Match the backend's MAX_IMAGE_SIZE (8 MB).
const MAX_FILE_SIZE = 8 * 1024 * 1024;

// ---- DOM refs -------------------------------------------------------------

document.addEventListener('DOMContentLoaded', function () {
    initPhotoUpload();
});

function initPhotoUpload() {
    const fileInput = document.getElementById('menu-photo-input');
    const uploadBtn = document.getElementById('upload-btn');
    const previewDiv = document.getElementById('photo-preview');
    const previewImg = document.getElementById('preview-image');
    const fileInfo = document.getElementById('file-info');
    const submitBtn = document.getElementById('upload-submit-btn');
    const removeBtn = document.getElementById('remove-photo-btn');
    const errorDiv = document.getElementById('upload-error');
    const successDiv = document.getElementById('upload-success');

    uploadBtn.addEventListener('click', function () {
        fileInput.click();
    });

    fileInput.addEventListener('change', function (e) {
        const file = e.target.files[0];

        errorDiv.style.display = 'none';
        successDiv.style.display = 'none';
        errorDiv.textContent = '';
        successDiv.textContent = '';

        if (!file) return;

        const validTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/heic', 'image/heif'];
        if (!validTypes.includes(file.type)) {
            showUploadError('Invalid format. Please upload JPEG, PNG, WEBP, or HEIC.');
            fileInput.value = '';
            return;
        }

        if (file.size > MAX_FILE_SIZE) {
            showUploadError(
                'File too large. Maximum size is 8 MB. Your file: '
                + (file.size / 1024 / 1024).toFixed(2) + ' MB'
            );
            fileInput.value = '';
            return;
        }

        const reader = new FileReader();
        reader.onload = function (event) {
            previewImg.src = event.target.result;
            fileInfo.textContent =
                '📄 ' + file.name + ' (' + (file.size / 1024 / 1024).toFixed(2) + ' MB)';
            previewDiv.style.display = 'block';
            uploadBtn.textContent = 'Choose another photo';
            submitBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    });

    submitBtn.addEventListener('click', async function () {
        const file = fileInput.files[0];
        if (!file) {
            showUploadError('Please select a photo first.');
            return;
        }

        submitBtn.textContent = 'Uploading...';
        submitBtn.disabled = true;
        errorDiv.style.display = 'none';
        successDiv.style.display = 'none';
        errorDiv.textContent = '';
        successDiv.textContent = '';

        try {
            const result = await uploadToServer(file);
            successDiv.textContent =
                '✅ Menu uploaded! Filename: ' + result.filename + '. Forwarded to OCR service.';
            successDiv.style.display = 'block';
            submitBtn.textContent = 'Sent for processing';
        } catch (err) {
            console.error('Upload failed:', err);
            showUploadError(
                'Upload failed: ' + (err && err.message ? err.message : 'network error')
            );
            submitBtn.textContent = 'Send for processing';
        } finally {
            submitBtn.disabled = false;
        }
    });

    removeBtn.addEventListener('click', function () {
        fileInput.value = '';
        previewDiv.style.display = 'none';
        previewImg.src = '#';
        fileInfo.textContent = '';
        uploadBtn.textContent = 'Choose Photo';
        errorDiv.style.display = 'none';
        successDiv.style.display = 'none';
        errorDiv.textContent = '';
        successDiv.textContent = '';
        submitBtn.textContent = 'Send for processing';
        submitBtn.disabled = false;
    });
}

function showUploadError(message) {
    const errorDiv = document.getElementById('upload-error');
    errorDiv.textContent = '⚠️ ' + message;
    errorDiv.style.display = 'block';
    document.getElementById('upload-success').style.display = 'none';
}

async function uploadToServer(file) {
    const formData = new FormData();
    // Field name must match the backend (`photo: UploadFile = File(...)`).
    formData.append('photo', file);

    const url = API_BASE_URL + '/upload-menu';
    const response = await fetch(url, {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        let detail = 'HTTP ' + response.status;
        try {
            const body = await response.json();
            if (body && body.detail) detail = body.detail;
        } catch (_) { /* keep generic detail */ }
        throw new Error(detail);
    }

    return await response.json();
}