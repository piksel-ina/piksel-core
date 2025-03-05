import pytest
from datacube import Datacube
import os
import yaml
from pathlib import Path

@pytest.fixture
def datacube_env():
    """
    Create a datacube environment for testing.
    
    Returns:
        Datacube: A datacube instance.
    """
    # Connect to the datacube
    try:
        dc = Datacube(app='piksel-test')
        return dc
    except Exception as e:
        pytest.skip(f"Could not connect to datacube: {str(e)}")

@pytest.fixture
def sample_product_definition():
    """
    Return a sample product definition for testing.
    
    Returns:
        dict: A dictionary containing a sample product definition.
    """
    # Create a simple test product definition
    return {
        "name": "test_product",
        "description": "A test product for unit testing",
        "metadata_type": "eo3",
        "metadata": {
            "product": {
                "name": "test_product"
            },
            "properties": {
                "eo:platform": "test",
                "eo:instrument": "test"
            }
        },
        "measurements": [
            {
                "name": "red",
                "dtype": "int16",
                "nodata": -999,
                "units": "1"
            },
            {
                "name": "nir",
                "dtype": "int16",
                "nodata": -999,
                "units": "1"
            }
        ],
        "storage": {
            "crs": "EPSG:4326",
            "resolution": {
                "longitude": 0.00025,
                "latitude": -0.00025
            }
        }
    }

@pytest.fixture
def product_definitions():
    """
    Load all product definitions from the products directory.
    
    Returns:
        dict: A dictionary mapping product names to their definitions.
    """
    products_dir = Path("products")
    if not products_dir.exists():
        return {}
    
    product_files = list(products_dir.glob("*.yaml"))
    products = {}
    
    for product_file in product_files:
        with open(product_file, 'r') as f:
            product_def = yaml.safe_load(f)
            products[product_def.get('name')] = product_def
    
    return products


def pytest_collection_modifyitems(items):
    """Modify test collection to ensure tests run in the correct order."""
    # Define a custom sort key to order our tests
    test_order = {
        "test_s2_index_data.py": 0,
        "test_s2_data_access.py": 1,
    }
    
    # Sort the items based on their module's position in test_order
    items.sort(key=lambda item: test_order.get(item.module.__file__.split('/')[-1], 100))
