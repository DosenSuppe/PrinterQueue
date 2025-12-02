# Printer Scheduler

## About
The Printer Scheduler is a small program created during a school project phase.

The `main`-branch contains the bare-minimum console version, while the `webapp` branch features a Flask web application with Tailwind CSS styling.

## Features
- Implementation of a queue data structure
- Add new print jobs
- View the next job in the queue
- View all jobs with pagination (5 per page)
- Perform/complete print jobs
- Modern web interface with Tailwind CSS (webapp branch)

## Installation

### Requirements
- Python 3.7+
- Flask (for webapp branch)

### Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd FinanceConsoleTool
   ```

2. Install dependencies:
   ```bash
   pip install flask
   ```

## Running the Application

### Console Version (main branch)
```bash
python Main.py
```

### Web Application (webapp branch)
```bash
python app.py
```

Then open your browser and navigate to:
```
http://127.0.0.1:5000
```

## Usage

### Web Interface
1. **Main Menu**: View all available options and total jobs in queue
2. **Add Job**: Enter a name for a new print job
3. **View Next Job**: See the next job to be processed
4. **View All Jobs**: Browse all jobs with pagination controls
5. **Perform Job**: Execute and remove the next job from the queue

