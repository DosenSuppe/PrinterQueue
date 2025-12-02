import json
from typing import List, BinaryIO
from formats.base import FormatHandler
from PrintJob import PrintJob


class JsonHandler(FormatHandler):
    
    @property
    def FormatName(self) -> str:
        return "JSON"
    
    @property
    def FileExtension(self) -> str:
        return ".json"
    
    @property
    def MimeType(self) -> str:
        return "application/json"
    
    def ExportJobs(self, Jobs: List[PrintJob]) -> bytes:
        Data = {
            "printQueue": {
                "version": "1.0",
                "jobs": [{"name": Job.name} for Job in Jobs]
            }
        }
        
        JsonString = json.dumps(Data, indent=2, ensure_ascii=False)
        
        return JsonString.encode('utf-8')
    
    def ImportJobs(self, Data: BinaryIO) -> List[PrintJob]:
        try:
            Content = Data.read().decode('utf-8')
            JsonData = json.loads(Content)
            
            if "printQueue" not in JsonData:
                raise ValueError("Invalid JSON format. Root object must contain 'printQueue'")
            
            PrintQueue = JsonData["printQueue"]
            
            if "jobs" not in PrintQueue:
                raise ValueError("Invalid JSON format. 'printQueue' must contain 'jobs' array")
            
            Jobs = []
            
            for JobData in PrintQueue["jobs"]:
                if not isinstance(JobData, dict):
                    raise ValueError("Invalid job data format. Each job must be an object")
                
                if "name" not in JobData:
                    raise ValueError("Invalid job object: Missing 'name' field")
                
                JobName = JobData["name"]
                if JobName is None or not str(JobName).strip():
                    continue
                
                Jobs.append(PrintJob(str(JobName).strip()))
            
            return Jobs
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {str(e)}")
        except UnicodeDecodeError:
            raise ValueError("Invalid file encoding. Please use UTF-8 encoded JSON files.")
        except Exception as e:
            raise ValueError(f"Error parsing JSON file: {str(e)}")