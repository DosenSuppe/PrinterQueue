import xml.etree.ElementTree as ET
import xml.dom.minidom
from typing import List, BinaryIO
from formats.base import FormatHandler
from PrintJob import PrintJob


class XmlHandler(FormatHandler):
    
    @property
    def FormatName(self) -> str:
        return "XML"
    
    @property
    def FileExtension(self) -> str:
        return ".xml"
    
    @property
    def MimeType(self) -> str:
        return "application/xml"
    
    def ExportJobs(self, Jobs: List[PrintJob]) -> bytes:
        Root = ET.Element("printQueue")
        Root.set("version", "1.0")
        
        for Job in Jobs:
            JobElement = ET.SubElement(Root, "job")
            NameElement = ET.SubElement(JobElement, "name")
            NameElement.text = Job.name
        
        RoughString = ET.tostring(Root, encoding='unicode')
        Reparsed = xml.dom.minidom.parseString(RoughString)
        PrettyXml = Reparsed.toprettyxml(indent="  ")
        
        Lines = [Line for Line in PrettyXml.split('\n') if Line.strip()]
        FormattedXml = '\n'.join(Lines)
        
        return FormattedXml.encode('utf-8')
    
    def ImportJobs(self, Data: BinaryIO) -> List[PrintJob]:
        try:
            Content = Data.read()
            Root = ET.fromstring(Content)
            
            if Root.tag != "printQueue":
                raise ValueError("Invalid XML format. Root element must be 'printQueue'")
            
            Jobs = []
            
            for JobElement in Root.findall("job"):
                NameElement = JobElement.find("name")
                
                if NameElement is None:
                    raise ValueError("Invalid job element: Missing 'name' element")
                
                JobName = NameElement.text
                if JobName is None or not JobName.strip():
                    continue
                
                Jobs.append(PrintJob(JobName.strip()))
            
            return Jobs
            
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML format: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error parsing XML file: {str(e)}")