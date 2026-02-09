"""
RGB-based styles for Sentinel-2 GeoMAD
"""

GEOMAD_S2_RGB = {
    "name": "rgb",
    "title": "Geomedian - Red, Green, Blue",
    "abstract": "True-colour image, using the red, green and blue bands",
    "components": {
      "red": {"red": 1.0}, 
      "green": {"green": 1.0}, 
      "blue": {"blue": 1.0}
      },
    "scale_range": [0.0, 3000.0],
    "multi_date": [
        {
          "allowed_count_range": [2, 4], 
          "animate": True
      }
    ],
}
