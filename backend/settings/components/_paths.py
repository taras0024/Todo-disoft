# -*- coding: utf-8 -*-
"""
Path settings shared by all platforms.
"""
import os
import sys

import backend as project_module
from backend.settings.tools import utils

PYTHON_BIN = os.path.dirname(sys.executable)
PROJECT_DIR = os.path.dirname(os.path.realpath(project_module.__file__))
PROJECT_ROOT = os.path.dirname(PROJECT_DIR)

APPS_ROOT = os.path.join(PROJECT_DIR, 'apps')
sys.path.append(APPS_ROOT)

VAR_ROOT = os.path.join(PROJECT_DIR, 'var')
LOG_ROOT = os.path.join(VAR_ROOT, 'log')

utils.create_directories(VAR_ROOT, LOG_ROOT)
