"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------
"""

import tank
import sys
import os

class SetContext(tank.platform.Application):
    
    def init_app(self):
        """
        Called as the application is being initialized
        """
        tk_multi_setcontext = self.import_module("tk_multi_setcontext")
        self.app_handler = tk_multi_setcontext.AppHandler(self)
        
        # add stuff to the context menu
        self.engine.register_command("Set Work Area...", 
                                     self.app_handler.show_dialog,
                                     {"type": "context_menu"})


        # only launch the dialog once at startup
        # use tank object to store this flag
        if not hasattr(tank, '_tk_multi_setcontext_shown'):
            # very first time we run this app
            tank._tk_multi_setcontext_shown = True
            # show the UI
            if self.get_setting('launch_at_startup'):
                self.app_handler.show_dialog()
