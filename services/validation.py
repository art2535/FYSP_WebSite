def validate_form(form_data):
    errors = {}

    if not form_data.get('name'):
        errors['name'] = 'Name is required'

    if not form_data.get('description'):
        errors['description'] = 'Description is required'

    if not form_data.get('phone'):
        errors['phone'] = 'Phone number is required'

    if not form_data.get('date'):
        errors['date'] = 'Date is required'

    return errors
