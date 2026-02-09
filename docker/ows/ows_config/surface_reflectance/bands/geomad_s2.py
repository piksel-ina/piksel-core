GEOMAD_S2_BANDS_INFO = {
    "blue": "Blue (490 nm)",
    "green": "Green (560 nm)",
    "red": "Red (665 nm)",
    "nir": "NIR (842 nm)",
    "swir16": "SWIR 1 (1610 nm)",
    "swir22": "SWIR 2 (2190 nm)",
    "SMAD": "Spectral Median Absolute Deviation",
    "EMAD": "Euclidean Median Absolute Deviation",
    "BCMAD": "Bray Curtis Median Absolute Deviation",
    "COUNT": "Number of observations in composite",
}


GEOMAD_S2_BANDS = {
    "blue": ["blue"],
    "green": ["green"],
    "red": ["red"],
    "nir": ["nir"],
    "swir16": ["swir16", "swir_16", "swir_1"],
    "swir22": ["swir22", "swir_22", "swir_2"],
    "SMAD": ["SMAD", "smad", "sdev", "SDEV"],
    "EMAD": ["EMAD", "emad", "edev", "EDEV"],
    "BCMAD": ["BCMAD", "bcmad", "bcdev", "BCDEV"],
    "COUNT": ["COUNT", "count"],
}
