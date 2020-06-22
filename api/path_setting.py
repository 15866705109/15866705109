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

# test_dyy_data.yaml
TEST_API_DATA = os.path.join(BASE_DIR, "testcase", "test_dyy_data.yaml")

#于超 test_yc_data.yaml
YUCHAO_TEST_DATA = os.path.join(BASE_DIR, "testcase", "test_yc_data.yaml")

# process_Data
PROCESS_DATA = os.path.join(BASE_DIR, "testcase", "process_data.yaml")