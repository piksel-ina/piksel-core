# test/integration/test_s2_data_access.py
import pytest
import xarray as xr
from datacube import Datacube
import numpy as np
import pickle
from pathlib import Path

# Use the same constants as in the indexing test
TEST_DATA_PATH = Path("/tmp/s2_test_data_info.pkl")

def test_load_sentinel2_data(datacube_env):
    """Test that we can load Sentinel-2 data using ODC from the indexed test area."""
    dc = Datacube(index=datacube_env.index)
    
    # Check if we have indexing information from the previous test
    if not TEST_DATA_PATH.exists():
        pytest.skip("No indexing info available. Run test_s2_index_data first.")
    
    # Load the indexing info
    with open(TEST_DATA_PATH, 'rb') as f:
        test_data_info = pickle.load(f)
    
    print(f"Using test data from: {test_data_info}")
    
    # Parse the bbox
    bbox_parts = test_data_info['bbox'].split(',')
    lon_min, lat_min, lon_max, lat_max = map(float, bbox_parts)
    
    # Parse the datetime
    time_parts = test_data_info['datetime'].split('/')
    time_range = tuple(time_parts)
    
    # Verify indexed data still exists
    datasets = dc.find_datasets(
        product='sentinel_2_l2a',
        lon=(lon_min, lon_max),
        lat=(lat_min, lat_max),
        time=time_range
    )
    
    if not datasets:
        pytest.skip(f"No Sentinel-2 datasets found in the test area. Expected {test_data_info['count']} datasets.")
    
    print(f"Found {len(datasets)} datasets, attempting to load data")
    
    try:
        # Load a small chip of data to verify it works
        data = dc.load(
            product='sentinel_2_l2a',
            lon=(lon_min, lon_max),
            lat=(lat_min, lat_max),
            time=time_range,
            measurements=['red', 'green', 'blue', 'nir'],
            resolution=(-0.0001, 0.0001),  # Load at lower resolution for faster test
            output_crs='EPSG:4326',
            dask_chunks={'time': 1, 'x': 512, 'y': 512}
        )
        
        # Check that we got valid data
        assert isinstance(data, xr.Dataset), "Data loading didn't return an xarray Dataset"
        print(f"Successfully loaded data with shape: {data.dims}")
        
        # Check that key bands exist
        for band in ['red', 'green', 'blue', 'nir']:
            assert band in data.data_vars, f"Band {band} missing from loaded data"
        
        # Check data dimensions
        assert data.dims['time'] > 0, "No time dimension in data"
        assert data.dims['x'] > 0, "No x dimension in data"
        assert data.dims['y'] > 0, "No y dimension in data"
        
        # Check that data has valid values (not all NaN)
        assert not np.isnan(data.red.values).all(), "Red band contains only NaN values"
        
        # Compute a small part to verify data can be read
        sample = data.red.isel(time=0).compute()
        print(f"Sample statistics - min: {sample.min().values}, max: {sample.max().values}")
        
    except Exception as e:
        pytest.fail(f"Failed to load Sentinel-2 data: {str(e)}")
