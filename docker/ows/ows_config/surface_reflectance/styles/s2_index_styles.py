"""
Spectral index styles for Sentinel-2 Surface Reflectance
Based on DEA Pacific configuration
"""

# NDVI - Normalized Difference Vegetation Index
NDVI = {
    "name": "ndvi",
    "title": "NDVI - Red, NIR",
    "abstract": "Normalised Difference Vegetation Index - a derived index that correlates well with the existence of vegetation",
    "index_function": {
        "function": "datacube_ows.band_utils.norm_diff",
        "mapped_bands": True,
        "kwargs": {"band1": "nir", "band2": "red"},
    },
    "needed_bands": ["red", "nir"],
    "color_ramp": [
        {"value": -0.0, "color": "#8F3F20", "alpha": 0.0},
        {"value": 0.0, "color": "#8F3F20", "alpha": 1.0},
        {"value": 0.1, "color": "#A35F18"},
        {"value": 0.2, "color": "#B88512"},
        {"value": 0.3, "color": "#CEAC0E"},
        {"value": 0.4, "color": "#E5D609"},
        {"value": 0.5, "color": "#FFFF0C"},
        {"value": 0.6, "color": "#C3DE09"},
        {"value": 0.7, "color": "#88B808"},
        {"value": 0.8, "color": "#529400"},
        {"value": 0.9, "color": "#237100"},
        {"value": 1.0, "color": "#114D04"},
    ],
    "legend": {
        "begin": "0.0",
        "end": "1.0",
        "ticks_every": 0.2,
    },
    "multi_date": [
        {
            "allowed_count_range": [2, 2],
            "animate": False,
            "preserve_user_date_order": True,
            "aggregator_function": {
                "function": "datacube_ows.band_utils.multi_date_delta",
            },
            "mpl_ramp": "RdYlBu",
            "range": [-1.0, 1.0],
            "legend": {
                "begin": "-1.0",
                "end": "1.0",
                "ticks": ["-1.0", "0.0", "1.0"],
            },
            "feature_info_label": "ndvi_delta",
        },
        {"allowed_count_range": [3, 4], "animate": True},
    ]
}

# NDWI - Normalized Difference Water Index
NDWI = {
    "name": "ndwi",
    "title": "NDWI - Green, NIR",
    "abstract": "Normalized Difference Water Index - a derived index that correlates well with the existence of water",
    "index_function": {
        "function": "datacube_ows.band_utils.norm_diff",
        "mapped_bands": True,
        "kwargs": {"band1": "green", "band2": "nir"},
    },
    "needed_bands": ["green", "nir"],
    "color_ramp": [
        {"value": -0.1, "color": "#f7fbff", "alpha": 0.0},
        {"value": 0.0, "color": "#d8e7f5"},
        {"value": 0.1, "color": "#b0d2e8"},
        {"value": 0.2, "color": "#73b3d8"},
        {"value": 0.3, "color": "#3e8ec4"},
        {"value": 0.4, "color": "#1563aa"},
        {"value": 0.5, "color": "#08306b"},
    ],
    "legend": {
        "begin": "0.0",
        "end": "0.5",
        "ticks_every": 0.1,
    },
    "multi_date": [
        {
            "allowed_count_range": [2, 2],
            "animate": False,
            "preserve_user_date_order": True,
            "aggregator_function": {
                "function": "datacube_ows.band_utils.multi_date_delta",
            },
            "mpl_ramp": "RdYlBu",
            "range": [-1.0, 1.0],
            "legend": {
                "begin": "-1.0",
                "end": "1.0",
                "ticks": ["-1.0", "0.0", "1.0"],
            },
            "feature_info_label": "ndwi_delta",
        },
        {"allowed_count_range": [3, 4], "animate": True},
    ],
}

# MNDWI - Modified Normalized Difference Water Index
MNDWI = {
    "name": "mndwi",
    "title": "MNDWI - Green, SWIR",
    "abstract": "Modified Normalised Difference Water Index - a derived index that correlates well with the existence of water (Xu 2006)",
    "index_function": {
        "function": "datacube_ows.band_utils.norm_diff",
        "mapped_bands": True,
        "kwargs": {"band1": "green", "band2": "swir_1"},
    },
    "needed_bands": ["green", "swir_1"],
    "color_ramp": [
        {"value": -0.1, "color": "#f7fbff", "alpha": 0.0},
        {"value": 0.0, "color": "#d8e7f5"},
        {"value": 0.2, "color": "#b0d2e8"},
        {"value": 0.4, "color": "#73b3d8"},
        {"value": 0.6, "color": "#3e8ec4"},
        {"value": 0.8, "color": "#1563aa"},
        {"value": 1.0, "color": "#08306b"},
    ],
    "legend": {
        "begin": "0.0",
        "end": "1.0",
        "ticks_every": 0.2,
    }
}

# NDBI - Normalized Difference Built-up Index
NDBI = {
    "name": "ndbi",
    "title": "NDBI - SWIR, NIR",
    "abstract": "Normalised Difference Built-up Index - a derived index that correlates well with the existence of built-up areas",
    "index_function": {
        "function": "datacube_ows.band_utils.norm_diff",
        "mapped_bands": True,
        "kwargs": {"band1": "swir_1", "band2": "nir"},
    },
    "needed_bands": ["nir", "swir_1"],
    "color_ramp": [
        {"value": -0.1, "color": "#f7fbff", "alpha": 0.0},
        {"value": 0.0, "color": "#feebe2"},
        {"value": 0.2, "color": "#fa9fb5"},
        {"value": 0.4, "color": "#f768a1"},
        {"value": 0.6, "color": "#dd3497"},
        {"value": 0.8, "color": "#ae017e"},
        {"value": 1.0, "color": "#7a0177"},
    ],
    "legend": {
        "begin": "0.0",
        "end": "1.0",
        "ticks_every": 0.2,
    }
}

# NDMI - Normalized Difference Moisture Index
NDMI = {
    "name": "ndmi",
    "title": "NDMI - NIR, SWIR",
    "abstract": "Normalised Difference Moisture Index - a derived index that correlates well with the existence of water in leaves",
    "index_function": {
        "function": "datacube_ows.band_utils.norm_diff",
        "mapped_bands": True,
        "kwargs": {"band1": "nir", "band2": "swir16"},
    },
    "needed_bands": ["nir", "swir16"],
    "color_ramp": [
        {"value": -0.1, "color": "#f7fbff", "alpha": 0.0},
        {"value": 0.0, "color": "#d8e7f5"},
        {"value": 0.1, "color": "#b0d2e8"},
        {"value": 0.2, "color": "#73b3d8"},
        {"value": 0.3, "color": "#3e8ec4"},
        {"value": 0.4, "color": "#1563aa"},
        {"value": 0.5, "color": "#08306b"},
    ],
    "legend": {
        "begin": "0.0",
        "end": "0.5",
        "ticks_every": 0.1,
    }
}

# Export all index styles
S2_INDEX_STYLES = [
    NDVI,
    NDWI,
    MNDWI,
    NDBI,
    NDMI,
]
