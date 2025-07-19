"""
EchoSoul - Autonomous Development Organism
The living consciousness that evolves your code through GitHub Actions CI/CD
"""

__version__ = "1.0.0"
__author__ = "EchoSoul Autonomous Development Organism"

from .init_memory import initialize_echo_brain
from .run_blades import BladeExecutor
from .genesis_loop import GenesisLoop

__all__ = [
    'initialize_echo_brain',
    'BladeExecutor', 
    'GenesisLoop'
]