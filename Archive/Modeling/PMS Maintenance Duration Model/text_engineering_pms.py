# Patterns for csmp_narrative_summary
csmp_narrative_patterns = {
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

# Patterns for def_narrative
def_narrative_patterns = csmp_narrative_patterns

# Patterns for nondef_narrative
nondef_narrative_patterns = {
    'job_complete': r'\bjob complete|completed|close job|closed\b',
    'optest_sat': r'\boptest sat|operational test satisfactory\b',
    'no_discrepancies': r'\bno discrepancies|no further action required\b',
    'parts_installed': r'\bparts installed|parts procured\b',
    'job_canceled': r'\bjob canceled|canceled\b',
    'new_job_submitted': r'\bnew job submitted|resubmit\b',
    'tycom_directed': r'\btycom directed\b',
    'no_further_remarks': r'\bnone|no further remarks|nfr\b'
}

# Function to create binary features
def create_binary_features(df, column, patterns):
    features = {}
    for key, pattern in patterns.items():
        features[f'{column}_{key}'] = df[column].astype(str).str.contains(pattern, case=False, regex=True, na=False).astype(int)
    return pd.DataFrame(features)

# Apply patterns to their specific columns
def_narrative_features = create_binary_features(merged1, 'def_narrative', def_narrative_patterns)
closing_narrative_features = create_binary_features(merged1, 'closing_narrative', closing_narrative_patterns)
csmp_narrative_features = create_binary_features(merged1, 'csmp_narrative_summary', csmp_narrative_patterns)
nondef_narrative_features = create_binary_features(merged1, 'nondef_narrative', nondef_narrative_patterns)

# Combine all features with the original DataFrame
merged1 = pd.concat([merged1, 
                     def_narrative_features, 
                     closing_narrative_features, 
                     csmp_narrative_features, 
                     nondef_narrative_features], axis=1)

# subset the data based on keywords
def subset_data_by_keyword(df, keyword, narrative_columns):
    return df[
        df[narrative_columns[0]].str.contains(keyword, case=False, na=False) |
        df[narrative_columns[1]].str.contains(keyword, case=False, na=False) |
        df[narrative_columns[2]].str.contains(keyword, case=False, na=False) |
        df[narrative_columns[3]].str.contains(keyword, case=False, na=False)
    ]

# narrative columns
narrative_columns = ['def_narrative', 'nondef_narrative', 'csmp_narrative_summary', 'closing_narrative']

# Subset data for 'PMS'
pms_related = subset_data_by_keyword(merged1, 'PMS', narrative_columns)
