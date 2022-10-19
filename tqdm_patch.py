import math
import sys
from reporting import post_progress

def patch_tqdm():
    from tqdm.auto import tqdm

    original_update = sys.modules['tqdm.auto'].tqdm.update
    original_iter = sys.modules['tqdm.auto'].tqdm.__iter__

    def new_update(self, n=1):
        original_update(self, n)
        perc = math.floor((self.n / self.total) * 100)
        if 'perc' not in self.__dict__ or perc != self.perc:
            if 'perc' not in self.__dict__:
                print("FIRST")
            self.perc = perc
            post_progress(self.desc, self.n, self.total)
            print(f"{self.desc} {perc} % ({self.n} / {self.total})")


    def new_iter(self):
        it = original_iter(self)
        print(">>> IT", it)
        for obj in it:
            print(">>> OB", obj)
            post_progress(obj, self.n, self.total)
            yield obj

    sys.modules['tqdm.auto'].tqdm.update = new_update
    sys.modules['tqdm.auto'].tqdm.__iter__ = new_iter
