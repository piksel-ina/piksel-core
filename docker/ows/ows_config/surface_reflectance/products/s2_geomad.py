"""
Sentinel-2 GeoMAD product configuration
"""
from ...common.resource_limits import GEOMAD_S2_LIMIT
from ..bands.geomad_s2 import GEOMAD_S2_BANDS_INFO, GEOMAD_S2_BANDS
from ..styles.geomad_s2 import GEOMAD_S2_RGB, GEOMAD_S2_NDVI

geomad_s2_annual_layer = {
    "title": "Annual GeoMAD (Sentinel-2)",
    "name": "geomad_s2_annual",
    "abstract": """ 
                GeoMAD (Geometric Median Absolute Deviation) statistics over Indonesia
                """,
    "product_name": "geomad_s2_annual",

    "resource_limits": GEOMAD_S2_LIMIT,
    
    "bands": GEOMAD_S2_BANDS,
    "feature_info": {
        "include_utc_dates": True,
        "include_bands": GEOMAD_S2_BANDS_INFO,
    },
    
    "dynamic": False,
    "time_resolution": "summary",

    "image_processing": {
        "extent_mask_func": ["ows_config.common.band_utils.mask_by_emad_nan"],
        "always_fetch_bands": ["emad"],
        "manual_merge": False,
        "apply_solar_corrections": False,
    },

    "native_crs": "EPSG:6933",
    "native_resolution": [10, -10],

    "styling": {
        "default_style": "rgb",
        "styles": [GEOMAD_S2_RGB, GEOMAD_S2_NDVI],
    },
}
