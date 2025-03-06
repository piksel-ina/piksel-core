import pytest
import time
import subprocess 
from dotenv import load_dotenv

def pytest_configure(config):
    config.addinivalue_line("markers", "dependency(name): mark test with dependencies")
    
@pytest.fixture(scope="session")
def datacube_environment():
    """Set up the datacube test environment."""
    # Start the containers
    subprocess.run(["make", "test-up"], check=True)
    
    # Wait for containers to be healthy (basic check)
    attempts = 0
    while attempts < 10:
        result = subprocess.run(
            ["docker", "inspect", "--format='{{.State.Health.Status}}'", "odc-test"],
            capture_output=True, text=True
        )
        if "healthy" in result.stdout:
            break
        time.sleep(3)
        attempts += 1
    
    # Now initialize datacube
    subprocess.run(
        ["docker", "exec", "odc-test", "datacube", "system", "init"],
        check=True
    )
    
    yield
    
    # Cleanup
    subprocess.run(["make", "test-down"])
