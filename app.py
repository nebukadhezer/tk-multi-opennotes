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
        import tk_multi_setcontext
        self.app_handler = tk_multi_setcontext.AppHandler(self)
        
        # add stuff to the context menu
        self.engine.register_command("Set Work Area...", 
                                     self.app_handler.show_dialog,
                                     {"type": "context_menu"})


