import os
import sys
import pytest

OWS_CONFIG_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'docker', 'ows')


@pytest.fixture(autouse=True, scope="module")
def _add_ows_to_path():
    ows_path = os.path.abspath(OWS_CONFIG_DIR)
    sys.modules.pop("ows_config", None)
    for key in list(sys.modules.keys()):
        if key.startswith("ows_config"):
            del sys.modules[key]
    sys.path.insert(0, ows_path)
    yield
    sys.path.remove(ows_path)


def test_ows_cfg_loads():
    from ows_config.ows_cfg import ows_cfg
    assert isinstance(ows_cfg, dict)
    assert "layers" in ows_cfg
    assert len(ows_cfg["layers"]) > 0


def test_s2_geomad_annual_layer_present():
    from ows_config.ows_cfg import ows_cfg
    layer_names = [l["name"] for l in ows_cfg["layers"]]
    assert "s2_geomad_annual" in layer_names


def test_s2_geomad_annual_layer_structure():
    from ows_config.ows_cfg import ows_cfg
    layer = next(l for l in ows_cfg["layers"] if l["name"] == "s2_geomad_annual")

    required_keys = ["title", "name", "abstract", "product_name", "bands",
                     "resource_limits", "native_crs", "native_resolution", "styling"]
    for key in required_keys:
        assert key in layer, f"Missing key: {key}"

    assert layer["product_name"] == "s2_geomad_annual"
    assert layer["native_crs"] == "EPSG:6933"
    assert layer["native_resolution"] == [10, -10]


def test_s2_geomad_annual_bands():
    from ows_config.ows_cfg import ows_cfg
    layer = next(l for l in ows_cfg["layers"] if l["name"] == "s2_geomad_annual")

    expected_bands = [
        "blue", "green", "red", "nir", "nir08",
        "rededge1", "rededge2", "rededge3",
        "swir16", "swir22", "SMAD", "EMAD", "BCMAD", "COUNT",
    ]
    assert set(layer["bands"].keys()) == set(expected_bands)


def test_s2_geomad_annual_styles():
    from ows_config.ows_cfg import ows_cfg
    layer = next(l for l in ows_cfg["layers"] if l["name"] == "s2_geomad_annual")

    assert "styling" in layer
    assert "default_style" in layer["styling"]
    assert "styles" in layer["styling"]
    assert layer["styling"]["default_style"] == "rgb"

    style_names = [s["name"] for s in layer["styling"]["styles"]]
    assert "rgb" in style_names
    assert "ndvi" in style_names
    assert "false_color_nir" in style_names
    assert "false_color_rededge" in style_names
    assert "ndvi_rededge" in style_names


def test_all_layer_styles_reference_valid_bands():
    from ows_config.ows_cfg import ows_cfg
    for layer in ows_cfg["layers"]:
        all_band_names = set()
        for key, aliases in layer["bands"].items():
            all_band_names.add(key)
            all_band_names.update(aliases)
        for style in layer["styling"]["styles"]:
            if "needed_bands" in style:
                for band in style["needed_bands"]:
                    assert band in all_band_names, (
                        f"Layer '{layer['name']}': style '{style['name']}' "
                        f"references band '{band}' not in defined bands or aliases"
                    )
