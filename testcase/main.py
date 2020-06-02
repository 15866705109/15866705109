'''
当需要分组执行用例时，可通过main入口运行
'''

import pytest

if __name__ == '__main__':
    pytest.main(["-m", "me"])