import pytest
import time
import subprocess
import os
from dotenv import load_dotenv

def pytest_configure(config):
    config.addinivalue_line("markers", "dependency(name): mark test with dependencies")
    
@pytest.fixture(scope="session")
def datacube_environment():
    """Set up the datacube test environment."""
    # Load environment variables
    env_file_path = os.path.join(os.path.dirname(__file__), '../.env')
    load_dotenv(env_file_path)
    
    # Start the containers with better error handling
    try:
        print("Starting test containers...")
        result = subprocess.run(["make", "test-up"], check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error starting containers: {e}")
        print(f"Command output: {e.stdout}")
        print(f"Command errors: {e.stderr}")
        pytest.fail("Failed to start test containers")
    
    # Wait for containers to be healthy with better logging
    attempts = 0
    max_attempts = 15
    while attempts < max_attempts:
        try:
            result = subprocess.run(
                ["docker", "inspect", "--format='{{.State.Health.Status}}'", "piksel-test-odc-1"],
                capture_output=True, text=True
            )
            if "healthy" in result.stdout:
                print(f"✓ Test containers ready after {attempts+1} attempts")
                break
        except subprocess.CalledProcessError:
            pass

        # Fallback: try running datacube directly even if healthcheck hasn't reported yet
        try:
            check = subprocess.run(
                ["docker", "exec", "piksel-test-odc-1", "datacube", "system", "check"],
                capture_output=True, text=True, timeout=15
            )
            if check.returncode == 0:
                print(f"✓ ODC container functional after {attempts+1} attempts (datacube check passed)")
                break
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            pass

        print(f"Waiting for containers ({attempts+1}/{max_attempts})...")
        time.sleep(5)
        attempts += 1

    if attempts >= max_attempts:
        pytest.fail("Test containers did not become healthy within timeout period")
    
    yield
    
    # Cleanup with better error handling
    try:
        print("Stopping test containers...")
        subprocess.run(["make", "test-down"], check=True, capture_output=True, text=True)
        print("Test containers stopped successfully")
    except subprocess.CalledProcessError as e:
        print(f"Warning: Error stopping containers: {e}")
        print(f"Command errors: {e.stderr}")

@pytest.fixture(scope="session", autouse=True)
def load_test_env():
    """Load environment variables once at beginning of test session."""
    env_path = os.path.join(os.path.dirname(__file__), '../.env')
    print(f"Loading environment from {env_path}")
    load_dotenv(env_path)
    return None
