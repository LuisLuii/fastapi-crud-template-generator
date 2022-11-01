from typing import Union


class ImportBuilder():
    def __init__(self):
        self.import_list = {}

    def add(self, *, import_: Union[set, str], from_: str = None):
        if isinstance(import_, str):
            import_ = set([import_])

        if from_ in self.import_list:
            self.import_list[from_] = self.import_list[from_] | import_
        else:
            self.import_list[from_] = import_

    def to_code(self):
        code = ""
        for from_path , import_name in self.import_list.items():
            sorted_list = list(import_name)
            sorted_list.sort()
            if not from_path:
                code += f"import {', '.join(sorted_list)}\n"
            else:
                code += f"from {from_path} import {', '.join(sorted_list)}\n"
        return code
