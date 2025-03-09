import yaml
import os

def test_sentinel2_product_definition():
    """Test that the Sentinel-2 product definition file exists and has required fields."""
    product_path = os.path.join('products', 's2_l2a.odc-product.yaml')
    assert os.path.exists(product_path), "Sentinel-2 product definition not found"
    
    with open(product_path, 'r') as f:
        product_def = yaml.safe_load(f)
    
    # Check required fields in the product definition
    assert 'name' in product_def, "Product name not defined"
    # Update this assertion to match the actual name in your YAML file
    # If the name in the YAML is 's2_l2a' instead of 'sentinel_2_l2a', update accordingly:
    assert product_def['name'] == 'sentinel_2_l2a', "Product name should be 's2_l2a'"
    assert 'description' in product_def, "Product description not defined"
    assert 'metadata_type' in product_def, "Metadata type not defined"
    assert 'measurements' in product_def, "Measurements not defined"
