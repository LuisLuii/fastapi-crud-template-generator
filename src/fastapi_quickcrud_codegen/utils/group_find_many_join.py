from itertools import groupby
from typing import List


def group_find_many_join(list_of_dict: List[dict]) -> List[dict]:
    def group_by_foreign_key(item):
        tmp = {}
        for k, v in item.items():
            if '_foreign' not in k:
                tmp[k] = v
        return tmp

    response_list = []
    for key, group in groupby(list_of_dict, group_by_foreign_key):
        response = {}
        for i in group:
            for k, v in i.items():
                if '_foreign' in k:
                    if k not in response:
                        response[k] = [v]
                    else:
                        response[k].append(v)
            for response_ in response:
                i.pop(response_, None)
            result = {**i, **response}
        response_list.append(result)
    return response_list
