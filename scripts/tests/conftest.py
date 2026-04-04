"""Common pytest fixtures and configuration."""

import sys
import os
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

logging.disable(logging.CRITICAL)
