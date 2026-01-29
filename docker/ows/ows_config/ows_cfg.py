"""
Main OWS configuration entry point
"""
from .ows_root_cfg import (
    service_title,
    service_abstract,
    service_keywords,
    contact_info,
    published_CRSs,
    allowed_urls,
    services,
    wms,
    wcs,
    ENABLE_SURFACE_REFLECTANCE,
)

layers = []

if ENABLE_SURFACE_REFLECTANCE:
    from .surface_reflectance import get_surface_reflectance_layers
    layers.extend(get_surface_reflectance_layers())

ows_cfg = {
    "global": {
        "response_headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "info_url": "",
        "fees": "",
        "access_constraints": "",
        "title": service_title,
        "abstract": service_abstract,
        "keywords": service_keywords,
        "contact_info": contact_info,
        "published_CRSs": published_CRSs,
        "allowed_urls": allowed_urls,
        "services": services,
    },
    "wms": wms,
    "wcs": wcs,
    "layers": layers,
}

if __name__ == "__main__":
    print(f"Service: {service_title}")
    print(f"Layers configured: {len(layers)}")
    for layer in layers:
        print(f"  - {layer['name']}: {layer['title']}")
        print(f"    Available Styles: {len(layer['styling']['styles'])}")
        print(f"    CRS: {layer['native_crs']}")
        print(f"    Resolution: {layer['native_resolution']}")
        print(f"    Default Style: {layer['styling']['default_style']}")
