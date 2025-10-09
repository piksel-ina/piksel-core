"""
RGB-based styles for Sentinel-2 Surface Reflectance
"""

s2_range = [0.0, 3000.0]

# True Color (Natural Color)
TRUE_COLOR = {
    "name": "simple_rgb",
    "title": "True Color - RGB",
    "abstract": "True color image using red, green and blue bands",
    "components": {
        "red": {"red": 1.0}, 
        "green": {"green": 1.0}, 
        "blue": {"blue": 1.0}
    },
    "scale_range": s2_range
}

# False Color (Vegetation) - NIR, Red, Green
FALSE_COLOR = {
    "name": "false_color",
    "title": "False Color - NIR, Red, Green",
    "abstract": "False color composite highlighting vegetation (NIR->Red, Red->Green, Green->Blue)",
    "components": {
        "red": {"nir": 1.0},    # NIR (B08)
        "green": {"red": 1.0},  # Red (B04)
        "blue": {"green": 1.0}  # Green (B03)
    },
    "scale_range": s2_range
}

# Infrared Green (SWIR, NIR, Green)
INFRARED_GREEN = {
    "name": "infrared_green",
    "title": "False Color - SWIR, NIR, Green",
    "abstract": "False color image with SWIR1->Red, NIR->Green, and Green->Blue",
    "components": {
        "red": {"swir16": 1.0},   # SWIR1 (B11)
        "green": {"nir": 1.0},    # NIR (B08)
        "blue": {"green": 1.0}    # Green (B03)
    },
    "scale_range": s2_range
}

# Agriculture (SWIR-NIR-Blue)
AGRICULTURE = {
    "name": "agriculture",
    "title": "Agriculture - SWIR, NIR, Blue",
    "abstract": "Agriculture composite (SWIR1->Red, NIR->Green, Blue->Blue)",
    "components": {
        "red": {"swir16": 1.0},   # SWIR1 (B11)
        "green": {"nir": 1.0},    # NIR (B08)
        "blue": {"blue": 1.0}     # Blue (B02)
    },
    "scale_range": s2_range
}

# Atmospheric Penetration (SWIR-SWIR-Red)
ATMOSPHERIC_PENETRATION = {
    "name": "atmospheric_penetration",
    "title": "Atmospheric Penetration - SWIR2, SWIR1, Red",
    "abstract": "SWIR composite for atmospheric penetration and smoke detection",
    "components": {
        "red": {"swir22": 1.0},   # SWIR2 (B12)
        "green": {"swir16": 1.0}, # SWIR1 (B11)
        "blue": {"red": 1.0}      # Red (B04)
    },
    "scale_range": s2_range
}

# Single band styles
BLUE_BAND = {
    "name": "blue",
    "title": "Blue - 490nm",
    "abstract": "Blue band (B02), centered on 490nm",
    "components": {
        "red": {"blue": 1.0},
        "green": {"blue": 1.0},
        "blue": {"blue": 1.0}
    },
    "scale_range": s2_range
}

GREEN_BAND = {
    "name": "green",
    "title": "Green - 560nm",
    "abstract": "Green band (B03), centered on 560nm",
    "components": {
        "red": {"green": 1.0},
        "green": {"green": 1.0},
        "blue": {"green": 1.0}
    },
    "scale_range": s2_range
}

RED_BAND = {
    "name": "red",
    "title": "Red - 665nm",
    "abstract": "Red band (B04), centered on 665nm",
    "components": {
        "red": {"red": 1.0},
        "green": {"red": 1.0},
        "blue": {"red": 1.0}
    },
    "scale_range": s2_range
}

NIR_BAND = {
    "name": "nir",
    "title": "Near Infrared (NIR) - 842nm",
    "abstract": "Near infrared band (B08), centered on 842nm",
    "components": {
        "red": {"nir": 1.0},
        "green": {"nir": 1.0},
        "blue": {"nir": 1.0}
    },
    "scale_range": s2_range
}

SWIR1_BAND = {
    "name": "swir_1",
    "title": "SWIR 1 - 1610nm",
    "abstract": "Short-wave infrared 1 band (B11), centered on 1610nm",
    "components": {
        "red": {"swir16": 1.0},
        "green": {"swir16": 1.0},
        "blue": {"swir16": 1.0}
    },
    "scale_range": s2_range
}

SWIR2_BAND = {
    "name": "swir_2",
    "title": "SWIR 2 - 2190nm",
    "abstract": "Short-wave infrared 2 band (B12), centered on 2190nm",
    "components": {
        "red": {"swir22": 1.0},
        "green": {"swir22": 1.0},
        "blue": {"swir22": 1.0}
    },
    "scale_range": s2_range
}

# Sentinel-2 specific: Red Edge bands
RED_EDGE_1 = {
    "name": "red_edge_1",
    "title": "Red Edge 1 - 705nm",
    "abstract": "Vegetation red edge band (B05), centered on 705nm",
    "components": {
        "red": {"rededge1": 1.0},
        "green": {"rededge1": 1.0},
        "blue": {"rededge1": 1.0}
    },
    "scale_range": s2_range
}

RED_EDGE_2 = {
    "name": "red_edge_2",
    "title": "Red Edge 2 - 740nm",
    "abstract": "Vegetation red edge band (B06), centered on 740nm",
    "components": {
        "red": {"rededge2": 1.0},
        "green": {"rededge2": 1.0},
        "blue": {"rededge2": 1.0}
    },
    "scale_range": s2_range
}

RED_EDGE_3 = {
    "name": "red_edge_3",
    "title": "Red Edge 3 - 783nm",
    "abstract": "Vegetation red edge band (B07), centered on 783nm",
    "components": {
        "red": {"rededge3": 1.0},
        "green": {"rededge3": 1.0},
        "blue": {"rededge3": 1.0}
    },
    "scale_range": s2_range
}

# Export all RGB styles
S2_RGB_STYLES = [
    TRUE_COLOR,
    FALSE_COLOR,
    INFRARED_GREEN,
    AGRICULTURE,
    ATMOSPHERIC_PENETRATION,
    BLUE_BAND,
    GREEN_BAND,
    RED_BAND,
    RED_EDGE_1,
    RED_EDGE_2,
    RED_EDGE_3,
    NIR_BAND,
    SWIR1_BAND,
    SWIR2_BAND,
]
