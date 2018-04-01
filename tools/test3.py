# -*- coding: utf-8 -*-

from pathlib import Path
from pprint import pprint
import os
import re

class Config():
    def __init__(self, params):
        self.params = params
    
    def search(self):
        pass


class sourceCode(Config):
    def __init__(self, params):
        super().__init__(params)
        self.path = params["path"]
        self.searchword = params["searchword"]
    
    def search(self):
        results = dict()
        path = Path(self.path)
        filenames = list(path.glob('**/*'))
        for filename in filenames:
            if os.path.isdir(filename):
                continue
            try:
                tmp_data = list()
                with  open(filename) as f:
                    lines = f.readlines()
                    tmp_data = [line for line in lines if len(re.findall(self.searchword, line)) > 0]
                if len(tmp_data) > 0:
                    results[filename] = tmp_data
            except:
                continue
        return results

if __name__ == '__main__':
    c = sourceCode({"path":"./prometheus", "searchword":r"prometheus|Prometheus"})
    results = c.search()
    for k,v in results.items():
        pprint("---------"+str(k)+"---------")
        pprint(v)
        pprint("-------------------------------------")
