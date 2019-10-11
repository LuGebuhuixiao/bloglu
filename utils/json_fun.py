from django.http import JsonResponse
from .res_code import Code


def to_json_data(errno=Code.OK, errmsg='', data=None, **kwargs):
    json_dict = {'errno': errno, 'errmsg': errmsg, 'data': data}

    if kwargs:
        json_dict.update(kwargs)

    return JsonResponse(json_dict)

# 错误信息函数
def err_msg(form):
    err_msg_list = []
    for item in form.errors.get_json_data().values():
        err_msg_list.append(item[0].get('message'))
    err_msg_str = '；'.join(err_msg_list)
    return err_msg_str