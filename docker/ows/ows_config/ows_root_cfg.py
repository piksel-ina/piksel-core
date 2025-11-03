# ows_root_cfg.py
"""
Root OWS configuration - global settings
"""

# Service metadata
service_title = "Indonesia OpenDataCube Web Services"
service_abstract = """
Earth observation data and derived products from Digital Earth Indonesia.
"""

service_keywords = [
    "digital earth",
    "digital earth indonesia",
    "datacube ows"
]

# Contact information
contact_info = {
    "person": "DE Indonesia Team",
    "organisation": "Digital Earth Indonesia",
    "position": "",
    "address": {
        "type": "postal",
        "address": "Badan Informasi Geospasial",
        "city": "Bogor",
        "state": "Jawa Barat",
        "postcode": "16920",
        "country": "Indonesia",
    },
    "email": "piksel@big.go.id",
    "telephone": "",  
    "fax": ""         
}

# Supported CRS
published_CRSs = {
    "EPSG:3857": {  # Web Mercator
        "geographic": False,
        "horizontal_coord": "x",
        "vertical_coord": "y",
    },
    "EPSG:4326": {  # WGS84
        "geographic": True,
        "vertical_coord_first": True
    },
    "EPSG:3577": {  # GDA-94, Australian Albers (required by datacube-ows)
        "geographic": False,
        "horizontal_coord": "x",
        "vertical_coord": "y",
    }
}

# Allowed URLs 
allowed_urls = [ 
    "http://localhost:8000",
    "http://127.0.0.1:8000",

    # Uncached OWS endpoint
    "https://ows-uncached.staging.pik-sel.id",
    "https://ows-uncached.pik-sel.id",
    
    # PUBLIC ENDPOINT
    "https://ows.staging.pik-sel.id",
    "https://ows.pik-sel.id",
]

# Enabled services
services = {
    "wms": True,
    "wcs": True,
    "wmts": True,
}

# Service-specific settings - Global settings for all products/layers/coverages
wms = {
    "max_width": 512,
    "max_height": 512,
    "caps_cache_maxage": 60 * 60,
}

wcs = {
    "default_geographic_CRS": "EPSG:4326",
    "formats": {
        "GeoTIFF": {
            "renderers": {
                "1": "datacube_ows.wcs1_utils.get_tiff", 
                "2": "datacube_ows.wcs2_utils.get_tiff", 
            },
            "mime": "image/geotiff",
            "extension": "tif",
            "multi-time": False,
        },
        "netCDF": {
            "renderers": {
                "1": "datacube_ows.wcs1_utils.get_netcdf", 
                "2": "datacube_ows.wcs2_utils.get_netcdf", 
            },
            "mime": "application/x-netcdf",
            "extension": "nc",
            "multi-time": True,
        },
    },
    "native_format": "GeoTIFF",
}

# Feature flags
ENABLE_SURFACE_REFLECTANCE = True
