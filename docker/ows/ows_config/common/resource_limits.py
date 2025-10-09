"""
Common resource limit configurations
"""

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
        "min_zoom_factor": 50.0,  # More restrictive due to 10m resolution
        "max_datasets": 4,
    },
    "wcs": {
        "max_datasets": 8,
    }
}
