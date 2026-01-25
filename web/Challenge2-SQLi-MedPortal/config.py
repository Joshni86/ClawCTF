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
    FLAG_VALUE = "CLAWCTF{data_can_cross_dimensions}"
    COMPANY_NAME = "Endurance Mission Control"
    COMPANY_SHORT = "EMC"
    COMPANY_YEAR = 2026


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
