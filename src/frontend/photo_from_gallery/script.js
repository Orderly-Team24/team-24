const MAX_FILE_SIZE = 5 * 1024 * 1024;

document.addEventListener('DOMContentLoaded', function() {
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

    uploadBtn.addEventListener('click', function() {
        fileInput.click();
    });

    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        
        errorDiv.style.display = 'none';
        successDiv.style.display = 'none';
        errorDiv.textContent = '';
        successDiv.textContent = '';
        
        if (!file) return;
        
        const validTypes = ['image/jpeg', 'image/png'];
        if (!validTypes.includes(file.type)) {
            showUploadError('Invalid format. Please upload JPEG or PNG.');
            fileInput.value = '';
            return;
        }
        
        if (file.size > MAX_FILE_SIZE) {
            showUploadError('File too large. Maximum size is 5 MB. Your file: ' + (file.size / 1024 / 1024).toFixed(2) + ' MB');
            fileInput.value = '';
            return;
        }
        
        const reader = new FileReader();
        reader.onload = function(event) {
            previewImg.src = event.target.result;
            fileInfo.textContent = '📄 ' + file.name + ' (' + (file.size / 1024 / 1024).toFixed(2) + ' MB)';
            previewDiv.style.display = 'block';
            uploadBtn.textContent = 'Choose another photo';
            submitBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    });

    submitBtn.addEventListener('click', function() {
        const file = fileInput.files[0];
        if (!file) {
            showUploadError('Please select a photo first.');
            return;
        }
        
        submitBtn.textContent = 'Processing...';
        submitBtn.disabled = true;
        errorDiv.style.display = 'none';
        successDiv.style.display = 'none';
        errorDiv.textContent = '';
        successDiv.textContent = '';
        
        setTimeout(function() {
            successDiv.textContent = '✅ Menu uploaded successfully! Processing... (demo)';
            successDiv.style.display = 'block';
            submitBtn.textContent = 'Sent for processing';
            submitBtn.disabled = false;
            
            console.log('File to upload:', file);
            console.log('File name:', file.name);
            console.log('File size:', file.size, 'bytes');
            console.log('File type:', file.type);
        }, 1500);
    });

    removeBtn.addEventListener('click', function() {
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
    formData.append('menu', file);
    
    try {
        const response = await fetch('/api/upload-menu', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Upload failed');
        }
        
        const result = await response.json();
        console.log('Server response:', result);
        return result;
    } catch (error) {
        console.error('Upload error:', error);
        throw error;
    }
}