"""
Sentinel-2 Surface Reflectance product configuration
"""

from ...common.resource_limits import SENTINEL2_LIMITS
from ..styles import S2_ALL_STYLES
from ..bands.sentinel2_bands import SENTINEL2_BANDS_INFO, SENTINEL2_BANDS

# Sentinel-2 Surface Reflectance Layer
s2_l2a_layer = {
    "title": "Sentinel-2 L2A Surface Reflectance",
    "abstract": """
    This layer is generated from Sentinel-2 L2A Surface Reflectance data harvested from a Sentinel-2 STAC catalogue and indexed into the Open Data Cube. The web services (WMS/WCS/WMTS) are produced on-the-fly from the indexed datacube. Rendering may be slower for large requests or for areas not previously requested due to geographic constraints during data retrieval.
    """,

    "keywords": [
        "sentinel",
        "sentinel-2",
        "setinel-2a",
        "surface reflectance",
        "s2_l2a",
        "sentinel 2",
    ],

    "name": "s2_l2a",
    "product_name": "s2_l2a",
    "default_time": "latest",


    "bands": SENTINEL2_BANDS,
    # "dynamic": True,

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
