from configparser import ConfigParser
class EDSConfigs:
    props = {}
    # default constructor
    def __init__(self):
        self.props = self._load_configs()
    def _load_configs(self):
        dict = {}
        config = ConfigParser()
        with open(r'~~folderpath~~/common/config/skill.properties') as f:
            config.read_string('[config]\n' + f.read())
        for k, v in config['config'].items():
            dict[k] = v
        return dict








