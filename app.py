import os
import logging
import pandas as pd
from flask import Flask, render_template, request, jsonify, flash, session
from hsn_validator import HSNValidator

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Initialize HSN Validator
hsn_validator = None

def load_hsn_data():
    global hsn_validator
    try:
        
        excel_file = "HSN_SAC.xlsx"
        hsn_df = pd.read_excel(excel_file)
        
        # Initialize validator with loaded data
        hsn_validator = HSNValidator(hsn_df)
        logger.info("HSN data loaded successfully")
    except Exception as e:
        logger.error(f"Error loading HSN data: {str(e)}")
        hsn_validator = None

# Load HSN data when application starts
load_hsn_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    if not hsn_validator:
        return jsonify({
            'valid': False,
            'message': 'HSN validator is not initialized. Please try again later.'
        }), 500
    
    hsn_code = request.form.get('hsn_code', '').strip()
    
    if not hsn_code:
        return jsonify({
            'valid': False,
            'message': 'HSN code is required'
        }), 400
    
    result = hsn_validator.validate(hsn_code)
    return jsonify(result)

@app.route('/batch_validate', methods=['POST'])
def batch_validate():
    if not hsn_validator:
        flash('HSN validator is not initialized. Please try again later.', 'danger')
        return render_template('index.html')
    
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return render_template('index.html')
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file', 'danger')
        return render_template('index.html')
    
    if not file.filename.endswith(('.csv', '.xlsx', '.xls')):
        flash('Invalid file format. Please upload a CSV or Excel file.', 'danger')
        return render_template('index.html')
    
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        if 'HSNCode' not in df.columns:
            flash('File must contain a column named "HSNCode"', 'danger')
            return render_template('index.html')
        
        # Validate each HSN code
        results = []
        for idx, row in df.iterrows():
            hsn_code = str(row['HSNCode']).strip()
            if hsn_code:
                result = hsn_validator.validate(hsn_code)
                results.append({
                    'hsn_code': hsn_code,
                    'valid': result['valid'],
                    'message': result['message'],
                    'description': result.get('description', '')
                })
        
        # Store results in session for display
        session['batch_results'] = results
        
        return render_template('batch_results.html', results=results)
    
    except Exception as e:
        logger.error(f"Error processing batch validation: {str(e)}")
        flash(f'Error processing file: {str(e)}', 'danger')
        return render_template('index.html')

@app.route('/batch_results')
def batch_results():
    results = session.get('batch_results', [])
    return render_template('batch_results.html', results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
