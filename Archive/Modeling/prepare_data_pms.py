import pandas as pd
import re

# Load your merged1 dataframe here
merged1 = pd.read_csv('merged1.csv')

# Define custom patterns for def_narrative and closing_narrative
def_narrative_patterns = {
    'maintenance_related': r'\bmaintenance|pm|preventive maintenance|inspection|check|routine\b',
    'repair_related': r'\brepair|troubleshoot|fix|correct\b',
    'replacement_related': r'\breplace|new|install|procure\b',
    'cleaning_related': r'\bclean|vacuum|wash\b',
    'corrosion_related': r'\bcorrosion|rust|preserve\b',
    'fan_related': r'\bfan\b',
    'coil_related': r'\bcoil\b',
    'filter_related': r'\bfilter\b',
    'motor_related': r'\bmotor\b',
    'valve_related': r'\bvalve\b',
    'switch_related': r'\bswitch\b',
    'belt_related': r'\bbelt\b'
}

closing_narrative_patterns = {
    'job_complete': r'\bjob complete|completed|close job|closed\b',
    'optest_sat': r'\boptest sat|operational test satisfactory\b',
    'no_discrepancies': r'\bno discrepancies|no further action required\b',
    'parts_installed': r'\bparts installed|parts procured\b',
    'job_canceled': r'\bjob canceled|canceled\b',
    'new_job_submitted': r'\bnew job submitted|resubmit\b',
    'tycom_directed': r'\btycom directed\b',
    'no_further_remarks': r'\bnone|no further remarks|nfr\b'
}

# Function to check if a job is canceled
def is_job_canceled(text):
    pattern = closing_narrative_patterns['job_canceled']
    return bool(re.search(pattern, str(text), re.IGNORECASE))

# Remove canceled jobs
merged1_filtered = merged1[~merged1['closing_narrative'].apply(is_job_canceled)]

# Print the number of rows removed
print(f"Number of rows removed: {len(merged1) - len(merged1_filtered)}")

# Update merged1 to the filtered version
merged1_filtered.to_csv('merged1_filtered.csv', index=False)

