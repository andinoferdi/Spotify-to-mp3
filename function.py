# function.py

import os

def clean_filename(filename):
    """Membersihkan nama file dari karakter yang tidak diinginkan."""
    return "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()

def setup_environment():
    """Memuat variabel lingkungan dari .env jika belum diatur."""
    from dotenv import load_dotenv
    load_dotenv()
