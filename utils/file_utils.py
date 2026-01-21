# utils/file_utils.py
import os
from config import SUPPORTED_FILE_TYPES

def is_supported_file(file_path):
    _, ext = os.path.splitext(file_path)
    return ext.lower() in SUPPORTED_FILE_TYPES

def get_file_size(file_path):
    return os.path.getsize(file_path)
