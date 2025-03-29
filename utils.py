import os
import glob

def get_available_months(journal_dir="data/journals"):
    """Get list of available journal months"""
    journal_files = glob.glob(os.path.join(journal_dir, "*.md"))
    # Extract month names from filenames (assuming format like '2025-02.md' or 'February2025.md')
    months = [os.path.basename(f).split('.')[0] for f in journal_files]
    return months

def load_journal(month, journal_dir="data/journals"):
    """Load journal content for a specific month"""
    file_path = os.path.join(journal_dir, f"{month}.md")
    if not os.path.exists(file_path):
        return "Journal not found for the selected month."
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content