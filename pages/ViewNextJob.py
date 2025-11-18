from .Page import Page

class ViewNextJob(Page):

    name = "View Next Job"
    
    def _InitPageLinks(self):
        if not (self._pageLinks is None):
            return
        
        from .Menu import Menu
        self._pageLinks = {
            '1': Menu(),
        }

    def _ShowFooter(self) -> None:
        print(self.footer)
        print("1: Back to Menu")

    def Display(self) -> None:
        nextJob = self.queue.Peek()

        if (nextJob is None):
            print("\nNo jobs in the queue.\n")
            self._ShowFooter()
            return
        
        print(f"\nNext Job: {nextJob.name}\n")
        self._ShowFooter()
    
    def HandleNextPage(self, pInput: str) -> 'Page':
        self._InitPageLinks()
        return self._pageLinks.get(pInput, None)