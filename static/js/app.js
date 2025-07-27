// Main JavaScript for Ollama Model Fine-Tuner

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Handle model download progress
    window.downloadModel = async function(modelId, button) {
        try {
            // Show loading state
            const originalText = button.innerHTML;
            button.disabled = true;
            button.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Downloading...';
            
            // Simulate download progress (replace with actual API call)
            const progressBar = document.getElementById(`progress-${modelId}`);
            let progress = 0;
            
            const interval = setInterval(() => {
                progress += 5;
                if (progress > 100) progress = 100;
                progressBar.style.width = `${progress}%`;
                progressBar.setAttribute('aria-valuenow', progress);
                
                if (progress === 100) {
                    clearInterval(interval);
                    button.innerHTML = '<i class="fas fa-check me-2"></i>Downloaded';
                    setTimeout(() => {
                        const modelCard = button.closest('.model-card');
                        modelCard.classList.add('border-success');
                        button.classList.remove('btn-primary');
                        button.classList.add('btn-success');
                        button.innerHTML = '<i class="fas fa-check me-2"></i>Downloaded';
                    }, 500);
                }
            }, 200);
            
            // Here you would make an actual API call to download the model
            // const response = await fetch(`/api/models/${modelId}/download`, { method: 'POST' });
            // const data = await response.json();
            
        } catch (error) {
            console.error('Error downloading model:', error);
            button.innerHTML = '<i class="fas fa-exclamation-triangle me-2"></i>Error';
            button.classList.remove('btn-primary');
            button.classList.add('btn-danger');
        }
    };

    // Handle model deletion
    window.deleteModel = async function(modelId, button) {
        if (!confirm('Are you sure you want to delete this model? This action cannot be undone.')) {
            return;
        }

        try {
            const card = button.closest('.model-card');
            card.style.opacity = '0.5';
            button.disabled = true;
            button.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Deleting...';
            
            // Here you would make an actual API call to delete the model
            // const response = await fetch(`/api/models/${modelId}`, { method: 'DELETE' });
            // const data = await response.json();
            
            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // Remove the card from the UI
            card.style.transition = 'all 0.3s ease';
            card.style.opacity = '0';
            setTimeout(() => card.remove(), 300);
            
            // Show success message
            showToast('Model deleted successfully', 'success');
            
        } catch (error) {
            console.error('Error deleting model:', error);
            showToast('Error deleting model', 'error');
            button.disabled = false;
            button.innerHTML = '<i class="fas fa-trash me-2"></i>Delete';
            const card = button.closest('.model-card');
            card.style.opacity = '1';
        }
    };

    // Show toast notification
    function showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toast-container');
        if (!toastContainer) return;
        
        const toast = document.createElement('div');
        toast.className = `toast show align-items-center text-white bg-${type} border-0`;
        toast.role = 'alert';
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;
        
        toastContainer.appendChild(toast);
        
        // Auto-remove toast after 5 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    }

    // Initialize all tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => {
        new bootstrap.Tooltip(tooltip);
    });

    // Handle tab switching
    const tabPanes = document.querySelectorAll('.tab-pane');
    const tabButtons = document.querySelectorAll('[data-bs-toggle="tab"]');
    
    tabButtons.forEach(button => {
        button.addEventListener('shown.bs.tab', function (e) {
            const target = document.querySelector(e.target.getAttribute('data-bs-target'));
            // Handle any tab-specific initialization here
        });
    });

    // Handle model search
    const searchInput = document.getElementById('model-search');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(function(e) {
            const query = e.target.value.trim();
            if (query.length > 2) {
                searchModels(query);
            } else {
                // Clear results if search query is too short
                const resultsContainer = document.getElementById('search-results');
                if (resultsContainer) {
                    resultsContainer.innerHTML = '';
                }
            }
        }, 300));
    }

    // Debounce function to limit API calls during search
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Search models function (to be implemented with actual API call)
    async function searchModels(query) {
        const resultsContainer = document.getElementById('search-results');
        if (!resultsContainer) return;
        
        // Show loading state
        resultsContainer.innerHTML = `
            <div class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2 text-muted">Searching for models...</p>
            </div>
        `;
        
        try {
            // Here you would make an actual API call to search for models
            // const response = await fetch(`/api/models/search?q=${encodeURIComponent(query)}`);
            // const data = await response.json();
            
            // Simulate API response
            await new Promise(resolve => setTimeout(resolve, 800));
            
            // Mock data - replace with actual API response
            const mockResults = [
                { id: 'llama2', name: 'LLaMA 2', description: 'Meta\'s latest large language model', size: '4.2 GB' },
                { id: 'mistral', name: 'Mistral 7B', description: 'High-quality text generation model', size: '3.8 GB' },
                { id: 'codellama', name: 'CodeLlama', description: 'Code generation and understanding', size: '5.1 GB' },
                { id: 'vicuna', name: 'Vicuna', description: 'Chat model fine-tuned from LLaMA', size: '4.5 GB' },
                { id: 'wizard', name: 'WizardLM', description: 'WizardLM language model', size: '4.8 GB' }
            ].filter(model => 
                model.name.toLowerCase().includes(query.toLowerCase()) ||
                model.description.toLowerCase().includes(query.toLowerCase())
            );
            
            // Display results
            if (mockResults.length > 0) {
                resultsContainer.innerHTML = mockResults.map(model => `
                    <div class="model-card card mb-3">
                        <div class="card-body">
                            <h5 class="card-title">${model.name}</h5>
                            <h6 class="card-subtitle mb-2 text-muted">${model.size}</h6>
                            <p class="card-text">${model.description}</p>
                            <button onclick="downloadModel('${model.id}', this)" class="btn btn-sm btn-primary">
                                <i class="fas fa-download me-2"></i>Download
                            </button>
                            <div class="progress mt-2 d-none" id="progress-${model.id}">
                                <div class="progress-bar" role="progressbar" style="width: 0%" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
                            </div>
                        </div>
                    </div>
                `).join('');
            } else {
                resultsContainer.innerHTML = `
                    <div class="text-center py-4">
                        <i class="fas fa-search fa-2x text-muted mb-3"></i>
                        <p class="text-muted">No models found matching "${query}"</p>
                    </div>
                `;
            }
            
        } catch (error) {
            console.error('Error searching models:', error);
            resultsContainer.innerHTML = `
                <div class="alert alert-danger" role="alert">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Error searching for models. Please try again later.
                </div>
            `;
        }
    }

    // Initialize any other components or event listeners here
    initializeDragAndDrop();
});

// Initialize drag and drop for file uploads
function initializeDragAndDrop() {
    const dropZone = document.getElementById('drop-zone');
    if (!dropZone) return;

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    dropZone.addEventListener('drop', handleDrop, false);

    function highlight() {
        dropZone.classList.add('border-primary', 'bg-light');
    }

    function unhighlight() {
        dropZone.classList.remove('border-primary', 'bg-light');
    }

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }
}

// Handle file uploads
function handleFiles(files) {
    const fileList = document.getElementById('file-list');
    if (!fileList) return;
    
    fileList.innerHTML = ''; // Clear previous files
    
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const fileItem = document.createElement('div');
        fileItem.className = 'list-group-item d-flex justify-content-between align-items-center';
        fileItem.innerHTML = `
            <div>
                <i class="fas fa-file me-2"></i>
                ${file.name}
                <small class="text-muted ms-2">${formatFileSize(file.size)}</small>
            </div>
            <button type="button" class="btn-close" aria-label="Remove file" onclick="this.parentElement.remove()"></button>
        `;
        fileList.appendChild(fileItem);
    }
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Initialize any Alpine.js components
document.addEventListener('alpine:init', () => {
    // Alpine.js components can be defined here
    Alpine.data('modelManager', () => ({
        models: [],
        isLoading: false,
        
        async fetchModels() {
            this.isLoading = true;
            try {
                const response = await fetch('/api/models');
                const data = await response.json();
                if (data.status === 'success') {
                    this.models = data.data || [];
                }
            } catch (error) {
                console.error('Error fetching models:', error);
            } finally {
                this.isLoading = false;
            }
        },
        
        init() {
            this.fetchModels();
        }
    }));
});
