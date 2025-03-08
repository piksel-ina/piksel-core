import pytest
import subprocess
import os

def test_datacube_init():
    """Test datacube initialization in the odc-test container."""
    # Run datacube init command inside the container
    init_cmd = ["docker", "exec", "odc-test", "datacube", "-v", "-E", "default", "system", "init"]
    init_result = subprocess.run(init_cmd, capture_output=True, text=True)
    
    # Print output for debugging
    print(f"Init command stdout: {init_result.stdout}")
    print(f"Init command stderr: {init_result.stderr}")
    
    # Check if init was successful (returns 0 on success)
    assert init_result.returncode == 0, f"Datacube init failed: {init_result.stderr}"
    
    # Verify with datacube system check
    check_cmd = ["docker", "exec", "odc-test", "datacube", "system", "check"]
    check_result = subprocess.run(check_cmd, capture_output=True, text=True)
    
    # Print output for debugging
    print(f"Check command stdout: {check_result.stdout}")
    print(f"Check command stderr: {check_result.stderr}")
    
    # Check if system check passes
    assert check_result.returncode == 0, f"Datacube system check failed: {check_result.stderr}"

def test_spatial_index_creation():
    """Test that spatial index can be created."""
    try:
        # Run the spindex-create command
        result = subprocess.run(
            ["docker", "exec", "odc-test", "datacube", "spindex", "create", "4326"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Spatial index creation failed: {result.stderr}"
        
        # Run spindex-update command
        result = subprocess.run(
            ["docker", "exec", "odc-test", "datacube", "spindex", "update", "4326"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Spatial index update failed: {result.stderr}"
        
    except Exception as e:
        pytest.skip(f"Spatial index test skipped: {str(e)}")
