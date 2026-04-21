"""
Styles for Sentinel-2 GeoMAD 14-band annual product
"""

S2_GEOMAD_14_RGB = {
    "name": "rgb",
    "title": "Geomedian - Red, Green, Blue",
    "abstract": "True-colour image, using the red, green and blue bands",
    "components": {
        "red": {"red": 1.0},
        "green": {"green": 1.0},
        "blue": {"blue": 1.0},
    },
    "scale_range": [0.0, 3000.0],
    "multi_date": [
        {
            "allowed_count_range": [2, 4],
            "animate": True,
        }
    ],
}

S2_GEOMAD_14_FALSE_COLOR = {
    "name": "false_color_nir",
    "title": "False Colour - NIR, Red, Green",
    "abstract": "False-colour image using NIR, red and green bands for vegetation analysis",
    "components": {
        "red": {"nir": 1.0},
        "green": {"red": 1.0},
        "blue": {"green": 1.0},
    },
    "scale_range": [0.0, 3000.0],
    "multi_date": [
        {
            "allowed_count_range": [2, 4],
            "animate": True,
        }
    ],
}

S2_GEOMAD_14_REDEDGE = {
    "name": "false_color_rededge",
    "title": "False Colour - Red Edge, NIR, Red",
    "abstract": "False-colour composite using red edge 2, NIR and red bands",
    "components": {
        "red": {"rededge2": 1.0},
        "green": {"nir": 1.0},
        "blue": {"red": 1.0},
    },
    "scale_range": [0.0, 3000.0],
    "multi_date": [
        {
            "allowed_count_range": [2, 4],
            "animate": True,
        }
    ],
}

S2_GEOMAD_14_NDVI = {
    "name": "ndvi",
    "title": "NDVI - Red, NIR",
    "abstract": "Normalised Difference Vegetation Index",
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
        "begin": 0.0,
        "end": 1.0,
        "ticks": [0.0, 0.5, 1.0],
    },
}

S2_GEOMAD_14_NDVI_RE = {
    "name": "ndvi_rededge",
    "title": "NDVI - Red Edge 1, NIR",
    "abstract": "Red Edge NDVI using red edge 1 and NIR narrow bands",
    "index_function": {
        "function": "datacube_ows.band_utils.norm_diff",
        "mapped_bands": True,
        "kwargs": {"band1": "nir08", "band2": "rededge1"},
    },
    "needed_bands": ["rededge1", "nir08"],
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
        "begin": 0.0,
        "end": 1.0,
        "ticks": [0.0, 0.5, 1.0],
    },
}
