"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------
"""
import tempfile
import os
import platform
import sys
import tank
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
        
        # special session handling for Nuke since nuke doesn't have a concept of
        # (re)loading a scene - it always starts a new process when a new file
        # is loaded.
        
        if self._app.engine.name == "tk-nuke":
            
            import nuke
            if nuke.root().name() != "Root":
                nuke.message("This App only works when you haven't yet opened a file. "
                             "Go to the Nuke menu, select File, New and then run the "
                             "App again from the empty scene.")
                return
        
        
        # do the import just before so that this app can run nicely in nuke
        # command line mode,
        from .dialog import AppDialog
        # must be nice to the GC here - attach this object
        # to something we know wont go away...
        self._dialog = tank.platform.qt.create_dialog(AppDialog)
        self._dialog.post_init(self._app)
        self._dialog.show()
        

