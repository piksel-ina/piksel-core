# test/conftest.py
import pytest
import datacube
import os

@pytest.fixture(scope="session")
def datacube_env():
    """Return a properly initialized datacube environment."""
    # Ensure we're using the test config
    os.environ.setdefault('DATACUBE_CONFIG_PATH', '/root/.datacube.conf')
    return datacube.Datacube()

@pytest.fixture(scope="session")
def odc_index(datacube_env):
    """Return the ODC index."""
    return datacube_env.index

@pytest.fixture
def sample_product_definition():
    """Return a test product definition."""
    return {
        "name": "test_product",
        "description": "Test product for unit tests",
        "metadata_type": "eo3",
        "measurements": [
            {"name": "red", "dtype": "int16", "nodata": -999},
            {"name": "nir", "dtype": "int16", "nodata": -999}
        ]
    }
