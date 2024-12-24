import streamlit as st
import pandas as pd
import re
import logging
from abc import ABC, abstractmethod
from typing import List, Dict
# Configure logging
logging.basicConfig(level=logging.INFO)
# Predefined regex patterns for common data formats
patterns = {
    "first_name": r'^[A-Z][a-z]{1,29}$',
    "last_name": r'^[A-Z][a-z]{1,29}$',
    "age": r'^(0|[1-9][0-9]|1[01][0-9]|120)$',  # Age pattern (0-120)
    "company_name": r'^[A-Z][a-zA-Z0-9\s,.&-]{1,49}$',
    "address": r'\d{1,5}\s[\w\s]+,\s[\w\s]+,\s[A-Za-z\s]+,\s\d{5}',
    "city": r'^[A-Z][a-zA-Z0-9\s,.&-]{1,49}$',
    "country": r'^[A-Z][a-zAZ0-9\s,.&-]{1,49}$',
    "phone": r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
    "date": r'\d{2}/\d{2}/\d{4}',
}

class FileHandler(ABC):
    """
    Abstract Base Class for handling file processing.
    """
    def __init__(self, file):
        self.file = file
        self.df = None
        self.regex_results = {}

    @abstractmethod
    def load_file(self):
        pass
    def get_sample_data(self, column_name: str) -> List[str]:
        """
        Get the first 10 non-null rows of the specified column.
        """
        if column_name in self.df.columns:
            return self.df[column_name].dropna().head(10).tolist()
        return []
    def match_column_patterns(self, column_name: str) -> Dict[str, str]:
        """
        Try to find regex patterns for the specified column.
        """
        sample_data = self.get_sample_data(column_name)
        
        for value in sample_data:
            match = self.match_patterns(value, column_name)
            if match:
                self.regex_results[column_name] = match
                break
        return self.regex_results
    def match_patterns(self, value: str, column_name: str) -> str:
        """
        Match the value against predefined or dynamic regex patterns.
        """
        if column_name in patterns:
            if re.match(patterns[column_name], str(value)):
                logging.info(f"Pattern matched for {column_name} with value {value}")
                return patterns[column_name]
        # Dynamically match patterns for specific columns
        if column_name == 'address':
            address_patterns = [
                r'\d{1,5}\s\w+(?:\s\w+)*,\s\w+(?:\s\w+)*,\s[A-Za-z\s]+,\s\d{5,6}',
                r'\d{1,5}\s\w+(?:\s\w+)*\s[A-Za-z\s]+,\s[A-Za-z\s]+,\s\d{5,6}',
            ]
            for pattern in address_patterns:
                if re.match(pattern, str(value)):
                    logging.info(f"Address pattern matched: {value}")
                    return pattern
        if column_name == 'date':
            date_patterns = [
                r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
                r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            ]
            for pattern in date_patterns:
                if re.match(pattern, str(value)):
                    logging.info(f"Date pattern matched: {value}")
                    return pattern
        if column_name == 'phone':
            phone_patterns = [
                r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', 
            ]
            for pattern in phone_patterns:
                if re.match(pattern, str(value)):
                    logging.info(f"Phone pattern matched: {value}")
                    return pattern
        if column_name == 'email':
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
            if re.match(email_pattern, str(value)):
                logging.info(f"Email pattern matched: {value}")
                return email_pattern
        logging.warning(f"No match found for column {column_name} with value {value}")
        return None

class CSVFileHandler(FileHandler):
    """
    Handles CSV file processing.
    """
    def load_file(self):
        try:
            self.df = pd.read_csv(self.file)
            logging.info(f"Loaded CSV file with {len(self.df)} rows.")
        except Exception as e:
            logging.error(f"Error loading CSV file: {e}")

class XLSXFileHandler(FileHandler):
    """
    Handles XLSX file processing.
    """
    def load_file(self):
        try:
            self.df = pd.read_excel(self.file)
            logging.info(f"Loaded XLSX file with {len(self.df)} rows.")
        except Exception as e:
            logging.error(f"Error loading XLSX file: {e}")

class FileProcessor:
    """
    Handles the file upload and processing logic.
    """
    def __init__(self, file):
        self.file = file
        self.handler = self.get_file_handler(file)
    def get_file_handler(self, file) -> FileHandler:
        if file.type == "text/csv":
            return CSVFileHandler(file)
        elif file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            return XLSXFileHandler(file)
        else:
            logging.error("Unsupported file format.")
            return None
    def process(self) -> Dict[str, str]:
        if self.handler:
            self.handler.load_file()
            regex_results = {}
            for column in self.handler.df.columns:
                column_results = self.handler.match_column_patterns(column)
                if column_results:
                    regex_results.update(column_results)
            return regex_results
        else:
            return {"error": "Unsupported file format"}

class LogManager:
    """
    Logs the details of file processing and pattern matching.
    """
    @staticmethod
    def log_summary(results: Dict[str, str]):
        if 'error' in results:
            logging.error(f"Processing failed: {results['error']}")
        else:
            logging.info("File processed successfully.")
            for column, pattern in results.items():
                logging.info(f"Column: {column} -> Matched Pattern: {pattern}")
# Streamlit File Upload and Result Display
st.title("Dynamic Regex Pattern Matching for CSV/XLSX")
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])
if uploaded_file is not None:
    processor = FileProcessor(uploaded_file)
    result = processor.process()
    LogManager.log_summary(result)
    if 'error' in result:
        st.error(result['error'])
    else:
        st.write("Generated Regex Patterns:")
        st.write(result)