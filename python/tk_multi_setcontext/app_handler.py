"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------
"""
import tempfile
import os
import platform
import sys
import uuid
import shutil


class AppHandler(object):
    """
    Handles the startup of the UIs, wrapped so that
    it works nicely in batch mode.
    """
    
    def __init__(self, app):
        self._app = app

    def show_dialog(self):
        
        
        # first make sure that this is a scene which hasn't been saved
        if nuke.root().name() != "Root":
            nuke.message("The set context app only works when you haven't yet opened a file. "
                         "Go to the Nuke menu, select File, New and then run the set context "
                         "app again from the empty scene.")
            
            return
        
        
        # do the import just before so that this app can run nicely in nuke
        # command line mode,
        from .dialog import AppDialog
        # must be nice to the GC here - attach this object
        # to something we know wont go away...
        self._dialog = AppDialog(self._app)
        self._dialog.show()
        

