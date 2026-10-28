"""
Vercel Serverless Function entrypoint for AI Ghost Story Generator.
Exposes the Flask WSGI application to Vercel's Python runtime.
"""
import sys
import os

# Add parent directory to sys.path so app can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
