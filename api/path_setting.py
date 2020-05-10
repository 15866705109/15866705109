import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

# api.yaml配置文件
APYAML_CONFIG = os.path.join(BASE_DIR, "api", "api.yaml")

# config.yaml
CONFIGYAML_CONFIG = os.path.join(BASE_DIR, "api", "config.yaml")

# host.yaml
HOSTYAML_CONFIG = os.path.join(BASE_DIR, "api", "host.yaml")

# cookie
GET_COOKIE = os.path.join(BASE_DIR, "api", "get_cookie.txt")
