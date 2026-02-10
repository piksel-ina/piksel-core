"""
Common resource limit configurations
"""

dataset_cache_rules = [
    {
        "min_datasets": 1,
        "max_age": 60 * 60 * 8,
    },
    {
        "min_datasets": 5,
        "max_age": 60 * 60 * 24,
    },
    {
        "min_datasets": 9,
        "max_age": 60 * 60 * 24 * 7,
    },
    {
        "min_datasets": 17,
        "max_age": 60 * 60 * 24 * 30,
    },
    {
        "min_datasets": 65,
        "max_age": 60 * 60 * 24 * 120,
    },
]

# Default limits for most products
DEFAULT_LIMITS = {
    "wms": {
        "zoomed_out_fill_colour": [150, 180, 200, 160],
        "min_zoom_factor": 35.0,
        "max_datasets": 6,
    },
    "wcs": {
        "max_datasets": 16,
    }
}

# For high-resolution products (Sentinel-2)
SENTINEL2_LIMITS = {
    "wms": {
        "zoomed_out_fill_colour": [150, 180, 200, 160],
        "min_zoom_factor": 50.0, 
        "dataset_cache_rules": dataset_cache_rules
    },
    "wcs": {
        "max_datasets": 8,
    }
}


GEOMAD_S2_LIMIT = {
    "wms": {
        "zoomed_out_fill_colour": [150, 180, 200, 160],
        "min_zoom_factor": 10.0,
        "dataset_cache_rules": dataset_cache_rules
    },
    "wcs": {
        "max_datasets": 32,
    },
}