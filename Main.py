import os

from Queue import Queue
from pages.Menu import Menu
from pages.AddJob import AddJob
from pages.ViewNextJob import ViewNextJob
from pages.ViewAllJobs import ViewAllJobs
from pages.PerformPrintJob import PerformPrintJob

queue = Queue()
currentPage = Menu(queue)

# initializing the pages (following the singleton pattern)
AddJob(queue)
ViewNextJob(queue)
ViewAllJobs(queue)
PerformPrintJob(queue)

def printPage() -> None:
    print(f"-- Printer Queue Tool // {currentPage.name} --")
    currentPage.Display()

while True:
    os.system('cls')
    printPage()
    choice = input("\nEnter next command: ")
    nextPage = currentPage.HandleNextPage(choice)

    if nextPage is not None:
        currentPage = nextPage