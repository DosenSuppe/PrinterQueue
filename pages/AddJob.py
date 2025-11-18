import sys
sys.path.insert(1, "../")

from PrintJob import PrintJob
from pages.Page import Page

class AddJob(Page):

    name = "Add Job"

    body = """\nPlease enter name for the new print job or the menu code.\n"""

    info = None
    
    def _InitPageLinks(self):
        if not (self._pageLinks is None):
            return
        
        from .Menu import Menu
        self._pageLinks = {
            '1': Menu(),
        }

    def Display(self) -> None:
        print(self.body)
        
        if (self.info is not None):
            print(self.info)
            self.info = None
        
        print(self.footer)
        print("1: Back to Menu (Cancel)")
    
    def HandleNextPage(self, pInput: str) -> 'Page':
        self.info = ""
        self._InitPageLinks()
        nextPage = self._pageLinks.get(pInput, None)

        if (nextPage is not None):
            return nextPage

        self.queue.Enqueue(PrintJob(pInput))
        self.info = f"Added new print job: {pInput}\n"

        return None
    



