from abc import ABC, abstractmethod
from typing import List, BinaryIO
from PrintJob import PrintJob


class FormatHandler(ABC):
    
    @property
    @abstractmethod
    def FormatName(self) -> str:
        pass
    
    @property
    @abstractmethod
    def FileExtension(self) -> str:
        pass
    
    @property
    @abstractmethod
    def MimeType(self) -> str:
        pass
    
    @abstractmethod
    def ExportJobs(self, Jobs: List[PrintJob]) -> bytes:
        pass
    
    @abstractmethod
    def ImportJobs(self, Data: BinaryIO) -> List[PrintJob]:
        pass