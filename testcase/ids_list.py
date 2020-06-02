from face_api_test.api import path_setting
from face_api_test.api.base_api import BaseApi


'''
此文件是用来将case转换成list
'''

def get_ids(data, path):
<<<<<<< HEAD

=======
>>>>>>> yuchao_branch_face
    params = data[path]
    case = []
    for ids in params:
        case.append(ids["case"])
    print('-@@@@@@@@@@@@',case,params)
    return case, params
