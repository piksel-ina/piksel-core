# In test/utils/validators.py:
def validate_product_document(doc):
    """
    A simplified validator for ODC product definitions.
    
    Args:
        doc (dict): The product definition document
        
    Returns:
        tuple: (is_valid, error_message)
    """
    # Check required top-level keys
    required_keys = ['name', 'description', 'metadata_type', 'measurements']
    
    for key in required_keys:
        if key not in doc:
            return False, f"Missing required field: {key}"
    
    # Check name is a string
    if not isinstance(doc['name'], str):
        return False, "Product name must be a string"
    
    # Check measurements is a dict or list
    if not isinstance(doc['measurements'], (dict, list)):
        return False, "Measurements must be a dict or list"
        
    # If measurements is a list of dicts, each must have a name
    if isinstance(doc['measurements'], list):
        for i, measurement in enumerate(doc['measurements']):
            if not isinstance(measurement, dict):
                return False, f"Measurement at index {i} must be a dictionary"
            if 'name' not in measurement:
                return False, f"Missing 'name' in measurement at index {i}"
    
    # If measurements is a dict, keys are measurement names
    elif isinstance(doc['measurements'], dict):
        for name, measurement in doc['measurements'].items():
            if not isinstance(measurement, dict):
                return False, f"Measurement '{name}' must be a dictionary"
    
    return True, "Valid product definition"
