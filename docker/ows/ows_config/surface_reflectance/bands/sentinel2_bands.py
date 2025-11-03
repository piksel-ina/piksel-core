"""
Sentinel-2 band definitions and metadata
"""

# Sentinel-2 band information for feature info
SENTINEL2_BANDS_INFO = {
    "B01": "Coastal aerosol (443 nm)",
    "B02": "Blue (490 nm)",
    "B03": "Green (560 nm)",
    "B04": "Red (665 nm)",
    "B05": "Red Edge 1 (705 nm)",
    "B06": "Red Edge 2 (740 nm)",
    "B07": "Red Edge 3 (783 nm)",
    "B08": "NIR (842 nm)",
    "B8A": "NIR Narrow (865 nm)",
    "B09": "Water vapor (945 nm)",
    "B11": "SWIR 1 (1610 nm)",
    "B12": "SWIR 2 (2190 nm)",
    "AOT": "Aerosol Optical Thickness",
    "WVP": "Scene Average Water Vapor",
    "SCL": "Scene Classification Layer - Quality information"
}

SENTINEL2_BANDS = {
    "B01": ["coastal_aerosol"],
    "B02": ["blue"],
    "B03": ["green"],
    "B04": ["red"],
    "B05": ["rededge1", "red_edge_1"],
    "B06": ["rededge2", "red_edge_2"],
    "B07": ["rededge3", "red_edge_3"],
    "B08": ["nir", "nir_1"],
    "B8A": ["nir_narrow", "nir_2"],
    "B09": ["water_vapour"],
    "B11": ["swir_1", "swir16"],
    "B12": ["swir_2", "swir22"],
    "AOT": ["aerosol_optical_thickness"],
    "WVP": ["scene_average_water_vapour"],
    "SCL": ["mask", "qa"],
}
