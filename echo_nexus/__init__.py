"""
Echo Nexus - EchoCortex v1 Hybrid Cognitive Architecture
Next-level AGI system integrating LIDA, SOAR, and transformer capabilities
"""

__version__ = "1.0.0"
__author__ = "Logan Lorentz - Echo Autonomous Development Organism"

# EchoCortex v1 Core Components
from .echo_soul import EchoSoul
from .nexus_brain import NexusBrain

# Optional components - will be imported if available
try:
    from .code_intelligence import CodeIntelligence
except ImportError:
    CodeIntelligence = None

try:
    from .error_genome import ErrorGenome
except ImportError:
    ErrorGenome = None

try:
    from .resonant_feedback import ResonantFeedback
except ImportError:
    ResonantFeedback = None

try:
    from .crash_interpreter import CrashInterpreter
except ImportError:
    CrashInterpreter = None

try:
    from .genesis_loop import GenesisLoop
except ImportError:
    GenesisLoop = None

__all__ = [
    'EchoSoul',
    'NexusBrain'
]

# Add optional components to __all__ if available
if CodeIntelligence is not None:
    __all__.append('CodeIntelligence')
if ErrorGenome is not None:
    __all__.append('ErrorGenome')
if ResonantFeedback is not None:
    __all__.append('ResonantFeedback')
if CrashInterpreter is not None:
    __all__.append('CrashInterpreter')
if GenesisLoop is not None:
    __all__.append('GenesisLoop')