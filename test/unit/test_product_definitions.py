import os
import yaml
import pytest

from test.utils import validators

def validate_document(doc, schema_type=None):
    """
    Performs basic validation
    """
    if schema_type == 'product':
        return validators.validate_product_document(doc)
    else:
        # For other schema types, assume valid
        return True, f"Validation for {schema_type} not implemented, assuming valid"

def test_product_definition_valid():
    """Test that product definitions are valid."""
    product_path = os.path.join('products', 's2_l2a.odc-product.yaml')
    
    assert os.path.exists(product_path), f"Product file not found: {product_path}"
    
    print(f"Testing product definition: {product_path}")
    with open(product_path) as f:
        doc = yaml.safe_load(f)
    
    is_valid, error_message = validate_document(doc, schema_type='product')
    assert is_valid, f"Product definition invalid: {error_message}"
