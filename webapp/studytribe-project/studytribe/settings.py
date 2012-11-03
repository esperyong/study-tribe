# -*- coding: utf-8 -*-
import os.path
import glob

try:
    STUDY_TRIBE_ROOT
except NameError:
    STUDY_TRIBE_ROOT = os.path.dirname(__file__)

conf_files_path = os.path.join(STUDY_TRIBE_ROOT, 
                               'settings', 
                               '*.conf')

conf_files = glob.glob(conf_files_path)

conf_files.sort()

for f in conf_files:
    execfile(os.path.abspath(f))

