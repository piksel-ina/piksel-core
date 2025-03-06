import os
import configparser

def test_datacube_config_exists():
    """Test that datacube.conf exists and has required sections."""
    assert os.path.exists('datacube.conf'), "datacube.conf file not found"
    
    config = configparser.ConfigParser()
    config.read('datacube.conf')
    
    assert 'default' in config, "Default section missing in datacube.conf"
    assert 'db_hostname' in config['default'], "db_hostname not found in config"
    assert 'db_username' in config['default'], "db_username not found in config"
    assert 'db_database' in config['default'], "db_database not found in config"
