from flask import Flask, request, render_template
import pandas as pd
import re
import logging

app = Flask(__name__)

# Predefined regex patterns for common data formats
patterns = {
    'date': [
        r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
        r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
        r'\d{2}-\d{2}-\d{4}',  # DD-MM-YYYY
    ],
    'phone': [
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # (XXX) XXX-XXXX or XXX-XXX-XXXX
        r'\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}',  # International format
    ],
    'email': [
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',  # Standard email
    ],
    'integer': [
        r'^\d+$',  # Positive integers
        r'^-?\d+$',  # Signed integers
    ],
    'float': [
        r'^\d*\.\d+$',  # Decimal numbers
        r'^-?\d*\.\d+$',  # Signed decimals
    ]
}

def load_url_data(url):
    try:
        return pd.read_html(url)[0]
    except Exception as e:
        logging.error(f"Error loading URL data: {e}")
        return pd.DataFrame()

def load_data(data_source, uploaded_file):
    try:
        if data_source == "CSV":
            return pd.read_csv(uploaded_file)
        elif data_source == "Excel":
            return pd.read_excel(uploaded_file)
        else:
            raise ValueError("Invalid data source")
    except Exception as e:
        logging.error(f"Error loading file data: {e}")
        return pd.DataFrame()

def match_patterns(value, pattern_list):
    for pattern in pattern_list:
        if re.match(pattern, str(value)):
            return pattern
    return None

def generate_regex_patterns(df):
    regex_patterns = {}
    for column in df.columns:
        column_values = df[column].dropna().unique()
        column_patterns = []
        
        for value in column_values:
            for data_type, type_patterns in patterns.items():
                matched_pattern = match_patterns(value, type_patterns)
                if matched_pattern:
                    column_patterns.append(matched_pattern)
                    break
        
        regex_patterns[column] = '|'.join(set(column_patterns)) if column_patterns else None
    return regex_patterns

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            data_source = request.form.get('data_source')
            uploaded_file = request.files.get('file')
            url = request.form.get('url')

            if data_source == "Enter URL" and url:
                df = load_url_data(url)
            elif uploaded_file:
                df = load_data(data_source, uploaded_file)
            else:
                return render_template('index.html', error="Please upload a file or enter a URL.")

            if not df.empty:
                regex_patterns = generate_regex_patterns(df)
                return render_template('results.html', df=df.to_html(index=False), regex_patterns=regex_patterns)
            else:
                return render_template('index.html', error="Failed to load data. Please check your input.")
        except Exception as e:
            logging.error(f"Error in POST request: {e}")
            return render_template('index.html', error="An unexpected error occurred.")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
