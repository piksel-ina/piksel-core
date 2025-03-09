import pytest
import subprocess
import time

def wait_for_container_health(container_name, max_retries=10, retry_interval=3):
    """Wait for container to become healthy with a retry mechanism."""
    for attempt in range(max_retries):
        result = subprocess.run(
            ['docker', 'inspect', '--format', '{{.State.Health.Status}}', container_name],
            capture_output=True,
            text=True
        )
        
        status = result.stdout.lower().strip()
        print(f"Attempt {attempt+1}/{max_retries}: Container {container_name} status: {status}")
        
        if 'healthy' in status:
            return True
            
        if attempt < max_retries - 1:
            print(f"Container not yet healthy, waiting {retry_interval} seconds...")
            time.sleep(retry_interval)
    
    return False

def test_postgres_container():
    """Test that the PostgreSQL test container is running and healthy."""
    container_name = "piksel-test-postgres-1"  # Your actual container name
    
    # Check that container exists
    result = subprocess.run(
        ['docker', 'ps', '-q', '--filter', f'name={container_name}'],
        capture_output=True,
        text=True
    )
    assert result.stdout.strip(), f"Postgres test container {container_name} not found"
    
    # Wait for container to become healthy
    is_healthy = wait_for_container_health(container_name)
    assert is_healthy, f"Postgres test container {container_name} did not become healthy within the timeout period"

def test_odc_container(datacube_environment):
    """Test that the ODC test container is running correctly."""
    
    # Verify odc container is running
    odc_status = subprocess.run(
        ["docker", "inspect", "--format", "{{.State.Status}}", "piksel-test-odc-1"],
        capture_output=True,
        text=True
    )
    assert "running" in odc_status.stdout.lower(), "ODC test container is not running"
    
    # Optional: Check ODC health if healthcheck is configured
    odc_health = subprocess.run(
        ["docker", "inspect", "--format", "{{if .State.Health}}{{.State.Health.Status}}{{else}}no-healthcheck{{end}}", "piksel-test-odc-1"],
        capture_output=True,
        text=True
    )
    if "no-healthcheck" not in odc_health.stdout.lower():
        assert "healthy" in odc_health.stdout.lower(), "ODC test container is not healthy"

def test_all_containers_running(datacube_environment):
    """List all piksel test containers for debugging purposes."""
    print("\nRunning test containers:")
    result = subprocess.run(
        ["docker", "ps", "--filter", "name=piksel-test"], 
        capture_output=True,
        text=True,
        check=True
    )
    print(result.stdout)
    assert result.returncode == 0, "Failed to list containers"
