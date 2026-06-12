#!/bin/bash
pip install packaging
python -c "from packaging import version;import sys;sys.exit(0 if version.parse('$1') > version.parse('$2') else 1)"
