"""
Configuration module for the Flask application.

Contains all application settings and configuration constants.
"""

import os


class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sqli-medical-supersecret-key'
    DEBUG = False
    
    # Database settings
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or 'users.db'
    
    # Server settings
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 5001))
    
    # Application settings
    FLAG_VALUE = "CLAWCTF{SQLi_Inj3ct0r_Pr0}"
    COMPANY_NAME = "Sacred Heart Medical Center"
    COMPANY_SHORT = "SHM"
    COMPANY_YEAR = 2025


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}
