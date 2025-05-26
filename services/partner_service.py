import os
import time
from services.file_service import load_json, save_json
from services.validation import validate_partner_form

def get_partners(data_file):
    """
    Load partner companies from the JSON file and sort them by name in alphabetical order.
    Returns a dictionary with the sorted list of companies.
    """
    companies = load_json(data_file) or []
    # Sort companies by name in alphabetical order (case-insensitive)
    companies.sort(key=lambda x: x['name'].lower())
    return {'companies': companies}

def add_partners(form_data, logo, data_file, upload_dir):
    """
    Process adding a new partner, including form validation and logo upload.
    Args:
        form_data: Form data from request.forms
        logo: Uploaded logo file from request.files
        data_file: Path to the JSON file for storing partners
        upload_dir: Directory for saving logo files
    Returns:
        Dictionary with companies, form_data, and errors.
    """
    # Extract form data
    form_data_dict = {
        'name': form_data.get('name', '').strip(),
        'description': form_data.get('description', '').strip(),
        'phone': form_data.get('phone', '').strip(),
        'date': form_data.get('date', '').strip(),
    }

    # Initialize return dictionary
    result = {
        'companies': load_json(data_file) or [],
        'form_data': form_data_dict,
        'errors': {}
    }

    # Handle logo upload
    filename = None
    if logo and logo.filename:
        name, ext = os.path.splitext(logo.filename.lower())
        if ext not in ('.png', '.jpg', '.jpeg'):
            result['errors']['logo'] = 'Invalid image format. Use PNG, JPG, or JPEG.'
            return result
        # Generate unique filename using timestamp
        timestamp = int(time.time() * 1000)  # Milliseconds for uniqueness
        filename = f"{name}_{timestamp}{ext}"
        try:
            logo.save(os.path.join(upload_dir, filename))
        except IOError as e:
            result['errors']['logo'] = f'Failed to save logo: {str(e)}'
            return result

    # Validate form data
    result['errors'] = validate_partner_form(form_data_dict)
    if result['errors']:
        return result

    # Add logo to form data and save to JSON
    form_data_dict['logo'] = filename if filename else ''
    result['companies'].append(form_data_dict)
    save_json(data_file, result['companies'])
    
    # Clear errors and form_data on successful save
    result['form_data'] = {}
    result['errors'] = {}
    return result