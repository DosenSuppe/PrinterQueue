from .Page import Page

class PerformPrintJob(Page):

    name = "Perform Print-Job"

    info = None
    
    def _InitPageLinks(self):
        if not (self._pageLinks is None):
            return
        
        from .Menu import Menu
        self._pageLinks = {
            '2': Menu(),
        }

    def _ShowFooter(self):
        if (self.info is not None):
            print(self.info)
            self.info = None

        print(self.footer)
        print("1. Perform Current Job \t\t2. Back to Menu (Cancel)")

    def Display(self) -> None:
        nextJob = self.queue.Peek()

        if (nextJob is None):
            print("No jobs in the queue.")
            self._ShowFooter()
            return
        
        print(f"Perform Job: {nextJob.name}")
        self._ShowFooter()
    
    def HandleNextPage(self, pInput: str) -> 'Page':
        self._InitPageLinks()
        page = self._pageLinks.get(pInput, None)

        if (page is not None):
            return page
        
        if (pInput == '1'):
            performedJob = self.queue.Dequeue()
            self.info = f"Performed Job: {performedJob.name if performedJob is not None else None}\n"

        return None