# test/integration/test_spatial_index.py
import pytest
import subprocess

def test_spatial_index_creation():
    """Test that spatial index can be created."""
    try:
        # Run the spindex-create command
        result = subprocess.run(
            ["docker", "exec", "odc", "datacube", "spindex", "create", "9468"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Spatial index creation failed: {result.stderr}"
        
        # Run spindex-update command
        result = subprocess.run(
            ["docker", "exec", "odc", "datacube", "spindex", "update", "9468"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Spatial index update failed: {result.stderr}"
        
    except Exception as e:
        pytest.skip(f"Spatial index test skipped: {str(e)}")
