import pytest
import subprocess
import os


PRODUCT_NAME = "s2_geomad_annual"
PRODUCT_FILE = os.path.join("products", "s2_geomad_annual.odc-product.yaml")
CONTAINER = "piksel-test-odc-1"
CONTAINER_PATH = f"/tmp/{os.path.basename(PRODUCT_FILE)}"


@pytest.mark.dependency(name="test_add_s2_geomad_annual_product", depends=["test_datacube_init"], scope="session")
def test_add_s2_geomad_annual_product(datacube_environment):
    assert os.path.exists(PRODUCT_FILE), f"Product definition not found: {PRODUCT_FILE}"

    subprocess.run(
        ["docker", "cp", PRODUCT_FILE, f"{CONTAINER}:{CONTAINER_PATH}"],
        check=True,
    )

    result = subprocess.run(
        ["docker", "exec", CONTAINER, "datacube", "product", "add", CONTAINER_PATH],
        capture_output=True,
        text=True,
    )

    print("\nProduct addition output:")
    print(result.stdout)
    if result.stderr:
        print("Product addition error:")
        print(result.stderr)

    assert result.returncode == 0, f"Product addition failed: {result.stderr}"

    verify = subprocess.run(
        ["docker", "exec", CONTAINER, "datacube", "product", "list"],
        capture_output=True,
        text=True,
    )
    assert PRODUCT_NAME in verify.stdout, f"{PRODUCT_NAME} not found in product list"


@pytest.mark.dependency(name="test_s3_to_dc_s2_geomad_annual", depends=["test_add_s2_geomad_annual_product"], scope="session")
def test_s3_to_dc_s2_geomad_annual(datacube_environment):
    cmd = [
        "docker", "exec", CONTAINER,
        "bash", "-c",
        "AWS_DEFAULT_REGION=ap-southeast-3 s3-to-dc --stac "
        "--no-sign-request "
        "--rename-product=s2_geomad_annual "
        "'s3://piksel-staging-public-data/geomad_s2/1.0.0/**/*.stac-item.json' "
        "s2_geomad_annual",
    ]

    print(f"\nRunning s3-to-dc for {PRODUCT_NAME}...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    print("Command output:")
    print(result.stdout)
    if result.stderr:
        print("Error output:")
        print(result.stderr)

    assert result.returncode == 0, f"s3-to-dc failed: {result.stderr}"
    assert "Added 0 Datasets" not in result.stdout, "No datasets were indexed"


@pytest.mark.dependency(name="test_s2_geomad_annual_dataset_count", depends=["test_s3_to_dc_s2_geomad_annual"], scope="session")
def test_s2_geomad_annual_dataset_count(datacube_environment):
    result = subprocess.run(
        ["docker", "exec", CONTAINER,
         "datacube", "dataset", "search",
         f"product={PRODUCT_NAME}"],
        capture_output=True,
        text=True,
    )

    print("\nDataset search output:")
    print(result.stdout)

    assert result.returncode == 0, f"Dataset search failed: {result.stderr}"
    assert len(result.stdout.strip()) > 0, "No datasets found for s2_geomad_annual"
