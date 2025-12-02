import csv
import io
from typing import List, BinaryIO
from formats.base import FormatHandler
from PrintJob import PrintJob


class CsvHandler(FormatHandler):
    
    @property
    def FormatName(self) -> str:
        return "CSV"
    
    @property
    def FileExtension(self) -> str:
        return ".csv"
    
    @property
    def MimeType(self) -> str:
        return "text/csv"
    
    def ExportJobs(self, Jobs: List[PrintJob]) -> bytes:
        Output = io.StringIO()
        Writer = csv.writer(Output)
        
        Writer.writerow(['Job Name'])
        
        for Job in Jobs:
            Writer.writerow([Job.name])
        
        CsvData = Output.getvalue()
        Output.close()
        
        return CsvData.encode('utf-8')
    
    def ImportJobs(self, Data: BinaryIO) -> List[PrintJob]:
        try:
            Content = Data.read().decode('utf-8')
            CsvFile = io.StringIO(Content)
            Reader = csv.reader(CsvFile)
            
            Jobs = []
            
            try:
                Header = next(Reader)
                if not Header or Header[0].lower() != 'job name':
                    raise ValueError("Invalid CSV format. Expected header 'Job Name'")
            except StopIteration:
                raise ValueError("Empty CSV file")
            
            for RowNum, Row in enumerate(Reader, start=2):
                if not Row:
                    continue
                
                if len(Row) < 1:
                    raise ValueError(f"Invalid row {RowNum}: Missing job name")
                
                JobName = Row[0].strip()
                if JobName:
                    Jobs.append(PrintJob(JobName))
            
            return Jobs
            
        except UnicodeDecodeError:
            raise ValueError("Invalid file encoding. Please use UTF-8 encoded CSV files.")
        except Exception as e:
            raise ValueError(f"Error parsing CSV file: {str(e)}")