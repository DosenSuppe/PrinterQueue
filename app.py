from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, Response
from Queue import Queue
from PrintJob import PrintJob
from ImportExportService import ImportExportService
import io

app = Flask(__name__)
app.secret_key = 'VerySecure'

# Initialize the queue and import/export service
queue = Queue()
ImportExportService = ImportExportService()

ENTRIES_PER_PAGE = 5

@app.route('/')
def Index():
    """Main menu page"""
    return render_template('Menu.html', QueueSize=queue.Size())

@app.route('/AddJob', methods=['GET', 'POST'])
def AddJob():
    """Add a new print job to the queue"""
    if request.method == 'POST':
        JobName = request.form.get('JobName', '').strip()
        if JobName:
            queue.Enqueue(PrintJob(JobName))
            flash(f'Added new print job: {JobName}', 'success')
            return redirect(url_for('AddJob'))
        else:
            flash('Please enter a job name', 'error')
    
    return render_template('AddJob.html')

@app.route('/ViewNext')
def ViewNext():
    """View the next job in the queue"""
    NextJob = queue.Peek()
    return render_template('ViewNext.html', NextJob=NextJob)

@app.route('/ViewAll')
def ViewAll():
    """View all jobs in the queue with pagination"""
    Page = request.args.get('Page', 1, type=int)
    TotalJobs = queue.Size()
    MaxPage = max(1, (TotalJobs + ENTRIES_PER_PAGE - 1) // ENTRIES_PER_PAGE)
    
    Page = max(1, min(Page, MaxPage))
    
    Jobs = []
    for i in range(ENTRIES_PER_PAGE):
        PageIndex = i + (Page - 1) * ENTRIES_PER_PAGE
        data = queue.PeekAt(PageIndex)
        Jobs.append({
            'Index': PageIndex + 1,
            'Name': data.name if data is not None else 'N/A'
        })
    
    return render_template('ViewAll.html', 
                         Jobs=Jobs, 
                         CurrentPage=Page, 
                         MaxPage=MaxPage,
                         TotalJobs=TotalJobs)

@app.route('/PerformJob', methods=['GET', 'POST'])
def PerformJob():
    """Perform the next print job"""
    if request.method == 'POST':
        PerformedJob = queue.Dequeue()
        if PerformedJob:
            flash(f'Performed Job: {PerformedJob.name}', 'success')
        else:
            flash('No jobs in the queue', 'error')
        return redirect(url_for('PerformJob'))
    
    NextJob = queue.Peek()
    return render_template('PerformJob.html', NextJob=NextJob)

@app.route('/ImportExport')
def ImportExport():
    """Import/Export page"""
    AvailableFormats = ImportExportService.GetAvailableFormats()
    return render_template('ImportExport.html', 
                         available_formats=AvailableFormats,
                         queue_size=queue.Size())

@app.route('/Export/<FormatName>')
def Export(FormatName):
    """Export queue to specified format"""
    try:
        ExportedData, Filename = ImportExportService.ExportQueue(queue, FormatName)
        Handler = ImportExportService.GetHandler(FormatName)
        
        return Response(
            ExportedData,
            mimetype=Handler.MimeType,
            headers={
                'Content-Disposition': f'attachment; filename="{Filename}"'
            }
        )
    except ValueError as e:
        flash(f'Export failed: {str(e)}', 'error')
        return redirect(url_for('ImportExport'))
    except Exception as e:
        flash(f'Unexpected error during export: {str(e)}', 'error')
        return redirect(url_for('ImportExport'))

@app.route('/Import', methods=['POST'])
def Import():
    """Import jobs from uploaded file"""
    try:
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('ImportExport'))
        
        File = request.files['file']
        if File.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('ImportExport'))
        
        FormatName = request.form.get('format', '').strip()
        ImportMode = request.form.get('mode', 'append')
        
        if not FormatName:
            flash('Please select a format', 'error')
            return redirect(url_for('ImportExport'))
        
        JobsCount = ImportExportService.ImportToQueue(
            queue, 
            io.BytesIO(File.read()), 
            FormatName, 
            ImportMode
        )
        
        ModeText = "replaced" if ImportMode == 'replace' else "added"
        flash(f'Successfully {ModeText} {JobsCount} job(s) from {File.filename}', 'success')
        
    except ValueError as e:
        flash(f'Import failed: {str(e)}', 'error')
    except Exception as e:
        flash(f'Unexpected error during import: {str(e)}', 'error')
    
    return redirect(url_for('ImportExport'))

if __name__ == '__main__':
    app.run(debug=True)
