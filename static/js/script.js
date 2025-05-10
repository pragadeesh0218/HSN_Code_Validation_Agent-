// Main JavaScript functionality for the HSN Code Validator

document.addEventListener('DOMContentLoaded', function() {
    // Handle single HSN code validation
    const singleValidationForm = document.getElementById('single-validation-form');
    const validationResults = document.getElementById('validation-results');
    
    if (singleValidationForm) {
        singleValidationForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            const hsn_code = document.getElementById('hsn_code').value.trim();
            
            if (!hsn_code) {
                showValidationResult({
                    valid: false,
                    message: 'Please enter an HSN code.'
                });
                return;
            }
            
            // Show loading state
            validationResults.innerHTML = '<div class="alert alert-info">Validating...</div>';
            
            // Send validation request
            fetch('/validate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    'hsn_code': hsn_code
                })
            })
            .then(response => response.json())
            .then(data => {
                showValidationResult(data);
            })
            .catch(error => {
                console.error('Error validating HSN code:', error);
                showValidationResult({
                    valid: false,
                    message: 'An error occurred while validating the HSN code. Please try again.'
                });
            });
        });
    }
    
    // Toggle between single and batch validation tabs
    const singleTab = document.getElementById('single-tab');
    const batchTab = document.getElementById('batch-tab');
    const singleValidationSection = document.getElementById('single-validation');
    const batchValidationSection = document.getElementById('batch-validation');
    
    if (singleTab && batchTab) {
        singleTab.addEventListener('click', function(event) {
            event.preventDefault();
            singleTab.classList.add('active');
            batchTab.classList.remove('active');
            singleValidationSection.classList.remove('d-none');
            batchValidationSection.classList.add('d-none');
        });
        
        batchTab.addEventListener('click', function(event) {
            event.preventDefault();
            batchTab.classList.add('active');
            singleTab.classList.remove('active');
            batchValidationSection.classList.remove('d-none');
            singleValidationSection.classList.add('d-none');
        });
    }
    
    // File input name display
    const batchFileInput = document.getElementById('batch_file');
    const fileLabel = document.querySelector('.custom-file-label');
    
    if (batchFileInput && fileLabel) {
        batchFileInput.addEventListener('change', function() {
            const fileName = this.files[0] ? this.files[0].name : 'Choose file';
            fileLabel.textContent = fileName;
        });
    }
});

// Display validation result with appropriate styling
function showValidationResult(result) {
    const validationResults = document.getElementById('validation-results');
    
    let alertClass = result.valid ? 'alert-success' : 'alert-danger';
    let icon = result.valid ? 
        '<i class="fas fa-check-circle me-2"></i>' : 
        '<i class="fas fa-exclamation-circle me-2"></i>';
    
    let html = `<div class="alert ${alertClass}">
                    ${icon}
                    <strong>${result.message}</strong>
                </div>`;
    
    // Add description if available
    if (result.valid && result.description) {
        html += `<div class="card mt-3">
                    <div class="card-header">
                        <h5 class="mb-0">HSN Description</h5>
                    </div>
                    <div class="card-body">
                        ${result.description}
                    </div>
                </div>`;
    }
    
    // Add parent code info if hierarchical validation
    if (result.valid && result.validation_type === 'hierarchical') {
        html += `<div class="alert alert-info mt-3">
                    <i class="fas fa-info-circle me-2"></i>
                    This code is valid because it follows the hierarchical structure under parent code: <strong>${result.parent_code}</strong>
                </div>`;
    }
    
    validationResults.innerHTML = html;
}
