import os
import sys
import re
import functools

class Rename:
    def __init__(self, sub_pattern, replacement, directory, recursive):
        self.sub_pattern = sub_pattern
        self.replacement = replacement
        self.directory = directory
        self.recursive = recursive
        self.num_files = 0
        self.to_change = {}
        self.changed = {}

    @staticmethod
    def _find(pattern, name):
        if re.search(pattern, name) is not None:
            return [name]
        else:
            return [None]

    def populate(self):
        if self.recursive:
            for root,_,files in os.walk(self.directory, topdown=True):
                self.to_change[root] = [x for y in list(map(lambda x: self._find(self.sub_pattern, x), files)) for x in y if x != None]
                self.changed[root] = list(map(lambda x: re.sub(self.sub_pattern, self.replacement, x), self.to_change[root]))
        else:
            files = [f for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))]
            self.to_change[self.directory] = [x for y in list(map(lambda x: self._find(self.sub_pattern, x), files)) for x in y if x != None]
            self.changed[self.directory] = list(map(lambda x: re.sub(self.sub_pattern, self.replacement, x), self.to_change[self.directory]))
        
        self.num_files = sum([len(x) for x in self.to_change.values()])

        print(self.to_change)
        return self.num_files

    def rename(self, incrementor=None):
        i = 0
        for root in self.to_change.keys():
            for before, after in zip(self.to_change[root], self.changed[root]):
                try:
                    os.rename(os.path.join(root, before), os.path.join(root, after))
                    i += 1
                    if incrementor:
                        bound_incrementor = functools.partial(incrementor, 100*int(round(i/self.num_files, 0)))
                        bound_incrementor()
                except Exception:
                    return False

        return True
            