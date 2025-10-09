"""
Styles for Surface Reflectance products
"""

from .s2_rgb_styles import S2_RGB_STYLES
from .s2_index_styles import S2_INDEX_STYLES

# Combined Sentinel-2 styles
S2_ALL_STYLES = S2_RGB_STYLES + S2_INDEX_STYLES

__all__ = [
    'S2_RGB_STYLES',
    'S2_INDEX_STYLES', 
    'S2_ALL_STYLES',
]
