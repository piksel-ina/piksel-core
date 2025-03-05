# test/integration/test_containers.py
import pytest
import subprocess
import os

def test_postgresql_container_running():
    """Test that the PostgreSQL container is running."""
    # Skip if not running in a container environment
    if not os.path.exists('/.dockerenv'):
        pytest.skip("This test only runs inside Docker")
    
    # Check if postgres container is accessible
    result = subprocess.run(
        ["pg_isready", "-h", "postgres", "-U", "piksel_user"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"PostgreSQL container is not ready: {result.stderr}"

def test_odc_container_configuration():
    """Test that ODC container is properly configured."""
    # Skip if not running in a container environment
    if not os.path.exists('/.dockerenv'):
        pytest.skip("This test only runs inside Docker")
    
    # Check if datacube.conf exists
    assert os.path.exists('/root/.datacube.conf'), "datacube.conf not found"
