"""
Echo Blades - Phase 1 Core Components
Simple, focused blades for essential operations
"""

__version__ = "1.0.0"
__author__ = "Echo Autonomous Development Organism"

# Phase 1 Core Blades
from .crash_parser import CrashParser
from .refactor_blade import RefactorBlade 
from .repair_engine import RepairEngine
from .git_connector import GitConnector

__all__ = [
    'CrashParser',
    'RefactorBlade', 
    'RepairEngine',
    'GitConnector'
]