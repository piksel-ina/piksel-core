# test/integration/test_docker_builds.py
import subprocess
import pytest
import os
from pathlib import Path

def test_all_images_build():
    """Test that all Docker images build without errors."""
    # Find the docker directory with docker-compose.yml
    project_root = Path(__file__).parent.parent.parent  # Go up to mini-piksel root
    docker_dir = project_root / "docker"
    
    # Verify docker-compose.yml exists
    docker_compose_path = docker_dir / "docker-compose.yml"
    assert docker_compose_path.exists(), f"Could not find docker-compose.yml at {docker_compose_path}"
    
    print(f"Running docker build test in {docker_dir}")
    
    # Run the build from the docker directory
    result = subprocess.run(
        ["docker", "compose", "build"],
        cwd=str(docker_dir),  # Set working directory to the docker folder
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Docker build failed: {result.stderr}"
