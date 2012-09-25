#!/usr/bin/env bash
# 
# Copyright (c) 2008 Shotgun Software, Inc
# ----------------------------------------------------

echo "building user interfaces..."
pyside-uic --from-imports dialog.ui > ../python/tk_multi_setcontext/ui/dialog.py
pyside-uic --from-imports new_task.ui > ../python/tk_multi_setcontext/ui/new_task.py

echo "building resources..."
pyside-rcc resources.qrc > ../python/tk_multi_setcontext/ui/resources_rc.py
