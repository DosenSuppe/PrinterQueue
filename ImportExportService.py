from typing import List, Dict, BinaryIO
from formats.base import FormatHandler
from formats.CsvHandler import CsvHandler
from formats.XmlHandler import XmlHandler
from formats.JsonHandler import JsonHandler
from PrintJob import PrintJob
from Queue import Queue


class ImportExportService:
    
    def __init__(self):
        self.Handlers: Dict[str, FormatHandler] = {}
        
        self.RegisterHandler(CsvHandler())
        self.RegisterHandler(XmlHandler())
        self.RegisterHandler(JsonHandler())
    
    def RegisterHandler(self, handler: FormatHandler) -> None:
        self.Handlers[handler.FormatName.upper()] = handler
    
    def GetAvailableFormats(self) -> List[Dict[str, str]]:
        Formats = []
        for Handler in self.Handlers.values():
            Formats.append({
                'name': Handler.FormatName,
                'extension': Handler.FileExtension,
                'mime_type': Handler.MimeType
            })
        return Formats
    
    def GetHandler(self, FormatName: str) -> FormatHandler:
        Handler = self.Handlers.get(FormatName.upper())
        if not Handler:
            Available = ', '.join(self.Handlers.keys())
            raise ValueError(f"Unsupported format '{FormatName}'. Available formats: {Available}")
        return Handler
    
    def ExportQueue(self, Queue: Queue, FormatName: str) -> tuple[bytes, str]:
        Handler = self.GetHandler(FormatName)
        
        Jobs = []
        Current = Queue.front
        while Current:
            Jobs.append(Current.data)
            Current = Current.next
        
        ExportedData = Handler.ExportJobs(Jobs)
        
        Filename = f"print_queue{Handler.FileExtension}"
        
        return ExportedData, Filename
    
    def ImportToQueue(self, Queue: Queue, Data: BinaryIO, FormatName: str, Mode: str = 'append') -> int:
        Handler = self.GetHandler(FormatName)
        
        ImportedJobs = Handler.ImportJobs(Data)
        
        if Mode == 'replace':
            while not Queue.IsEmpty():
                Queue.Dequeue()
        elif Mode != 'append':
            raise ValueError(f"Invalid import mode '{Mode}'. Use 'append' or 'replace'")
        
        for Job in ImportedJobs:
            Queue.Enqueue(Job)
        
        return len(ImportedJobs)