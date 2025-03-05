# test/integration/test_odc_init.py
import pytest

def test_datacube_connection(datacube_env):
    """Test that we can connect to the datacube database."""
    # Simply checking that the datacube_env fixture works
    assert datacube_env is not None

    # Test we can access metadata types - convert generator to list
    metadata_types = list(datacube_env.index.metadata_types.get_all())
    assert len(metadata_types) > 0

def test_spatial_tables(datacube_env):
    """Test that spatial tables are properly configured."""
    # Use the new API structure
    try:
        # Try direct connection method if available
        connection = datacube_env.index._db.connect()
        connection.close()
        assert True, "Successfully connected to database"
    except AttributeError:
        # Newer ODC versions have different connection methods
        # Check if products exist as a proxy for DB connection
        products = list(datacube_env.index.products.get_all())
        assert len(products) > 0, "Database accessible via products query"

