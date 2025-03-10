# tests/integration/test_stac_index_s2_l2a.py
import pytest
import subprocess
import os

@pytest.mark.dependency(depends=["test_datacube_init"])
def test_add_sentinel2_product(datacube_environment):
    """Add the Sentinel-2 L2A product definition to the datacube."""
    # Path to the existing product definition file
    product_file = os.path.join('products', 's2_l2a.odc-product.yaml')
    assert os.path.exists(product_file), "Product definition file not found"
    
    # Copy the product definition to the container
    container_path = "/tmp/s2_l2a.odc-product.yaml"
    subprocess.run(
        ["docker", "cp", product_file, f"piksel-test-odc-1:{container_path}"],
        check=True
    )
    
    # Add the product to datacube
    cmd = [
        "docker", "exec", "piksel-test-odc-1",
        "datacube", "product", "add", container_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print("\nProduct addition output:")
    print(result.stdout)
    
    if result.stderr:
        print("Product addition error:")
        print(result.stderr)
        
    # Check if product addition was successful
    assert result.returncode == 0, f"Product addition failed: {result.stderr}"
    
    # Verify the product exists
    verify_cmd = [
        "docker", "exec", "piksel-test-odc-1",
        "datacube", "product", "list"
    ]
    
    verify_result = subprocess.run(verify_cmd, capture_output=True, text=True)
    assert "sentinel_2_l2a" in verify_result.stdout, "Product was not added successfully"

@pytest.mark.dependency(depends=["test_add_sentinel2_product"])
def test_stac_to_dc_sentinel2_indonesia(datacube_environment):
    """Test indexing Sentinel-2 data from STAC for a small region in Indonesia."""
    # Define a small area in Indonesia (Bali area)
    bbox = "115.1,-8.4,115.3,-8.2"
    date_range = "2022-01-01/2022-01-15"
    collection = "sentinel-2-l2a"
    product_name = "sentinel_2_l2a"
    
    # Run the stac-to-dc command in the test container
    cmd = [
        "docker", "exec", "piksel-test-odc-1",
        "stac-to-dc", 
        "--catalog-href=https://earth-search.aws.element84.com/v1/",
        f"--bbox={bbox}",
        f"--collections={collection}",
        f"--datetime={date_range}",
        f"--rename-product={product_name}",
        "--limit=5"  # Limit results to keep test fast
    ]
    
    print(f"\nRunning stac-to-dc command with parameters:")
    print(f"  - bbox: {bbox} (small area in Bali, Indonesia)")
    print(f"  - date range: {date_range}")
    print(f"  - collection: {collection}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Print output for debugging
    print("Command output:")
    print(result.stdout)
    
    if result.stderr:
        print("Error output:")
        print(result.stderr)
    
    # Check if indexing was successful
    assert result.returncode == 0, f"STAC-to-DC indexing failed: {result.stderr}"
    
    # Verify we actually added some datasets
    assert "Added 0 Datasets" not in result.stdout, "No datasets were added during indexing"
