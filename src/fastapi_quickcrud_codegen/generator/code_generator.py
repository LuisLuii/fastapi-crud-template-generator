import os
import sys

from ..misc.constant import GENERATION_FOLDER


class CodeGenerator:
    def __init__(self):
        dirname, _ = os.path.split(os.path.abspath(sys.argv[0]))
        self.current_directory = dirname
        self.template_root_directory = os.path.join(self.current_directory, GENERATION_FOLDER)
        self.module_path_map = {}