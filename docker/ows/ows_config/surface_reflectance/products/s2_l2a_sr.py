"""
Sentinel-2 Surface Reflectance product configuration
"""

from ...common.resource_limits import SENTINEL2_LIMITS
from ..styles import S2_ALL_STYLES
from ..bands.sentinel2_bands import SENTINEL2_BANDS_INFO, SENTINEL2_BANDS

# Sentinel-2 Surface Reflectance Layer
s2_l2a_layer = {
    "title": "Sentinel-2 L2A Surface Reflectance",
    "name": "s2_l2a",
    "abstract": """
    Sentinel-2 Level-2A Surface Reflectance product.
    Atmospherically corrected surface reflectance from the MSI sensor.
    10m spatial resolution for visible and NIR bands, 5-day revisit over Indonesia.
    """,

    "product_name": "s2_l2a",
    "bands": SENTINEL2_BANDS,
    "dynamic": True,
    
    # Spatial configuration
    "native_crs": "EPSG:3857",  
    "native_resolution": [10.0, -10.0], 

    # Image processing
    "image_processing": {
        "extent_mask_func": "datacube_ows.ogc_utils.mask_by_val",
        "always_fetch_bands": [],
        "manual_merge": False,
        "apply_solar_corrections": False
    },
    
    # Styling configuration
    "styling": {
        "default_style": "simple_rgb",
        "styles": S2_ALL_STYLES,
    },
    
    # Resource limits
    "resource_limits": SENTINEL2_LIMITS,
    
    # Feature info (GetFeatureInfo response)
    "feature_info": {
        "include_utc_dates": True,
        "include_bands": SENTINEL2_BANDS_INFO,
    },
    
    # Time dimension
    "time_resolution": "solar",
}
