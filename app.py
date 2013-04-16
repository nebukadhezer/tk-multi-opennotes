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
        cb = lambda : tk_multi_setcontext.show_dialog(self)
        # add stuff to the context menu
        self.engine.register_command("set_work_area", cb, {"type": "context_menu", "title": "Set Work Area..."})

        # only launch the dialog once at startup
        # use tank object to store this flag
        if not hasattr(tank, '_tk_multi_setcontext_shown'):
            # very first time we run this app
            tank._tk_multi_setcontext_shown = True
            # show the UI at startup, but only if engine supports a UI
            if self.get_setting('launch_at_startup') and self.engine.has_ui:
                tk_multi_setcontext.show_dialog(self)
