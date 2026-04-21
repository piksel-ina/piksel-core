"""
Sentinel-2 GeoMAD 14-band annual product configuration
"""
from ...common.resource_limits import GEOMAD_S2_LIMIT
from ..bands.s2_geomad_14band import S2_GEOMAD_14_BANDS_INFO, S2_GEOMAD_14_BANDS
from ..styles.s2_geomad_14band import (
    S2_GEOMAD_14_RGB,
    S2_GEOMAD_14_FALSE_COLOR,
    S2_GEOMAD_14_REDEDGE,
    S2_GEOMAD_14_NDVI,
    S2_GEOMAD_14_NDVI_RE,
)

s2_geomad_annual_layer = {
    "title": "Annual GeoMAD 14-band (Sentinel-2)",
    "name": "s2_geomad_annual",
    "abstract": """
                GeoMAD (Geometric Median Absolute Deviation) statistics over Indonesia
                (full 14-band including nir08, red edge bands)
                """,
    "product_name": "s2_geomad_annual",

    "resource_limits": GEOMAD_S2_LIMIT,

    "bands": S2_GEOMAD_14_BANDS,
    "feature_info": {
        "include_utc_dates": True,
        "include_bands": S2_GEOMAD_14_BANDS_INFO,
    },

    "dynamic": False,
    "time_resolution": "summary",

    "image_processing": {
        "extent_mask_func": ["ows_config.common.band_utils.mask_by_emad_nan"],
        "always_fetch_bands": ["EMAD"],
        "manual_merge": False,
        "apply_solar_corrections": False,
    },

    "native_crs": "EPSG:6933",
    "native_resolution": [10, -10],

    "styling": {
        "default_style": "rgb",
        "styles": [
            S2_GEOMAD_14_RGB,
            S2_GEOMAD_14_FALSE_COLOR,
            S2_GEOMAD_14_REDEDGE,
            S2_GEOMAD_14_NDVI,
            S2_GEOMAD_14_NDVI_RE,
        ],
    },
}
