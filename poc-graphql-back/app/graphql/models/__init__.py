from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

"""
    Registering Tables in the database
"""

from .stickynotes import StickyNote
from .users import User
