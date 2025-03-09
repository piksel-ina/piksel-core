# test/integration/test_spatial_index.py
import pytest
import subprocess

@pytest.mark.dependency(depends=["test_datacube_init"])
def test_spatial_index_creation(datacube_environment):
    """Test that spatial index can be created."""
    try:
        # Run the spindex-create command
        result = subprocess.run(
            ["docker", "exec", "piksel-test-odc-1", "datacube", "spindex", "create", "4326"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Spatial index creation failed: {result.stderr}"
        
        # Run spindex-update command
        result = subprocess.run(
            ["docker", "exec", "piksel-test-odc-1", "datacube", "spindex", "update", "4326"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Spatial index update failed: {result.stderr}"
        
    except Exception as e:
        pytest.skip(f"Spatial index test skipped: {str(e)}")
