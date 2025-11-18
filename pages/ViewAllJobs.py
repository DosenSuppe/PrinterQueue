from .Page import Page

ENTRIES_PER_PAGE = 5

class ViewAllJobs(Page):

    name = "View All Jobs"

    currentPage = 1
    
    def _InitPageLinks(self):
        if not (self._pageLinks is None):
            return
        
        from .Menu import Menu
        self._pageLinks = {
            '0': Menu(),
        }

    def _GetMaxPage(self) -> int:
        return (self.queue.Size() + ENTRIES_PER_PAGE - 1) // ENTRIES_PER_PAGE or 1

    def Display(self) -> None:
        for i in range(ENTRIES_PER_PAGE):
            pageIndex = i + (self.currentPage - 1) * ENTRIES_PER_PAGE
            data = self.queue.PeekAt(pageIndex)
            print(f"{pageIndex + 1}. {data.name if data is not None else 'N/A'}")

        print(self.footer)
        print(f"Page {self.currentPage} of {self._GetMaxPage()} | Total Jobs: {self.queue.Size()}")
        print(self.footer)

        print("1: Next Page \t\t 2: Previous Page")
        print("0: Back to Menu")

    def HandleNextPage(self, pInput: str) -> 'Page':
        self._InitPageLinks()
        page = self._pageLinks.get(pInput, None)

        if (page is not None):
            return page
        
        if (pInput == '1'):
            self.currentPage = min(self.currentPage + 1, self._GetMaxPage())
        elif (pInput == '2'):
            self.currentPage = max(self.currentPage - 1, 1)

        return None