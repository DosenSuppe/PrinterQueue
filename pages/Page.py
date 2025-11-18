import sys
sys.path.insert(1, "../")

from Queue import Queue

class Page(object):
    name: str = "N/A NAME"
    body: str = "N/A BODY"
    footer: str = "-----------------------------------"
    queue: Queue = None

    _pageLinks: dict[str, 'Page'] = None

    def __new__(cls, pQueue=None):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Page, cls).__new__(cls)
            cls.instance.queue = pQueue
        return cls.instance

    def _InitPageLinks(self):
        pass

    def HandleNextPage(self, pInput: str) -> 'Page':
        self._initPageLinks()
        return self._pageLinks.get(pInput, None) 

    def Display(self) -> None:
        print(self.body)
        print(self.footer)