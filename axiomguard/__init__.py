"""
Axion Guard - AI Security and Governance Platform
=================================================

A comprehensive security platform for AI systems providing:
- Instruction leak detection
- Prompt injection analysis
- Bias detection
- Behavioral anomaly analysis
- Governance and compliance tools

Version: 0.1.0
Author: Axion Team
"""

__version__ = "0.1.0"
__author__ = "Axion Team"

from .core.guard import AxionGuard
from .core.analyzer import SecurityAnalyzer

__all__ = ["AxionGuard", "SecurityAnalyzer"]

