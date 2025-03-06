import docker
import pytest
import time
import subprocess

@pytest.fixture
def docker_client():
    return docker.from_env()

@pytest.mark.dependency() # Mark this test as a dependency for other tests
def test_postgres_container_starts(docker_client):
    """Test that the PostgreSQL container starts correctly."""
    # This test remains unchanged as it's working correctly
    container = docker_client.containers.run(
        "postgis/postgis:16-3.5",
        detach=True,
        environment={
            "POSTGRES_USER": "test_user",
            "POSTGRES_DB": "test_db",
            "POSTGRES_PASSWORD": "test_password"
        }
    )
    
    # Wait for container to start
    time.sleep(5)
    
    # Check container status
    container.reload()
    assert container.status == "running"
    
    # Cleanup
    container.stop()
    container.remove()

@pytest.mark.dependency(depends=["test_postgres_container_starts"])
def test_odc_container_starts():
    """Test that the ODC container starts correctly using direct Docker commands."""
    # Debug print of all running containers to verify test environment
    all_containers = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True,
        text=True
    )
    print(f"\nAll running containers: {all_containers.stdout}")
    
    # Check if odc-test container is running
    result = subprocess.run(
        ["docker", "inspect", "--format", "{{.State.Status}}", "odc-test"],
        capture_output=True,
        text=True
    )
    
    # Print the result for debugging
    print(f"Container status: '{result.stdout.strip()}'")
    
    # Assert container is running
    assert "running" in result.stdout.lower(), "ODC container is not running"
