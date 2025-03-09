import pytest
import subprocess
import os

# This test is responsible for initializing the datacube
@pytest.mark.dependency()
def test_datacube_init(datacube_environment):
    """Test datacube initialization in the odc container."""
    # Run datacube init command inside the container
    init_cmd = ["docker", "exec", "piksel-test-odc-1", "datacube", "-v", "-E", "default", "system", "init"]
    init_result = subprocess.run(init_cmd, capture_output=True, text=True)
    
    # Print output for debugging
    print(f"Init command stdout: {init_result.stdout}")
    print(f"Init command stderr: {init_result.stderr}")
    
    # Check if init was successful (returns 0 on success)
    assert init_result.returncode == 0, f"Datacube init failed: {init_result.stderr}"
    
    # Verify with datacube system check
    check_cmd = ["docker", "exec", "piksel-test-odc-1", "datacube", "system", "check"]
    check_result = subprocess.run(check_cmd, capture_output=True, text=True)
    
    # Print output for debugging
    print(f"Check command stdout: {check_result.stdout}")
    print(f"Check command stderr: {check_result.stderr}")
    
    # Check if system check passes
    assert check_result.returncode == 0, f"Datacube system check failed: {check_result.stderr}"
    
    # Verify postgis driver is being used (similar to production)
    # Fix the shell parameter inconsistency
    driver_cmd = "docker exec piksel-test-odc-1 bash -c \"datacube system check | grep 'Index Driver'\""
    driver_result = subprocess.run(driver_cmd, capture_output=True, text=True, shell=True)
    assert "postgis" in driver_result.stdout, "PostGIS driver not used in test environment"
