def patch_usgs_landsat(url: str) -> str:
    """
    Patch the USGS Landsat URL to use S3:// instead of HTTPS://.

    Args:
        url (str): The original URL.

    Returns:
        str: The patched URL.
    """
    return url.replace("https://landsatlook.usgs.gov/data", "s3://usgs-landsat")
