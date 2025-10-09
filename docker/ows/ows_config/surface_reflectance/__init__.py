"""
Surface reflectance product configurations
"""

from .products.s2_l2a_sr import s2_l2a_layer

def get_surface_reflectance_layers():
    """Get all surface reflectance layers"""
    return [
        s2_l2a_layer,
    ]

__all__ = ['get_surface_reflectance_layers']
