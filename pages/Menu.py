
from .Page import Page

class Menu(Page):

    name = "Menu"

    body = """\nControls:
    1 : View next print job
    2 : View all print jobs

    3 : Perform next print job
    4 : Add new print job
    
    5 : Exit\n"""
    
    def _InitPageLinks(self):
        if not (self._pageLinks is None):
            return
        
        from .ViewNextJob import ViewNextJob
        from .ViewAllJobs import ViewAllJobs
        from .PerformPrintJob import PerformPrintJob
        from .AddJob import AddJob

        self._pageLinks = {
            '1': ViewNextJob(),
            '2': ViewAllJobs(),
            '3': PerformPrintJob(),
            '4': AddJob(),
        }

    def HandleNextPage(self, pInput: str) -> 'Page':
        self._InitPageLinks()
        page = self._pageLinks.get(pInput, None)

        if (page is not None):
            return page
        
        if (pInput == '5'):
            exit(0)

     
