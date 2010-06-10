import logging

import gobject

from webkit import WebView as WebkitWebView

class WebView(WebkitWebView):
    __gtype_name__ = "WebView"
    __gsignals__ = {
        'is-setup': (gobject.SIGNAL_RUN_FIRST,
                  gobject.TYPE_NONE,
                  ([]))
    }
    
    def __init__(self):
        WebkitWebView.__init__(self)
        
        self.set_full_content_zoom(True)
        
    def do_setup(self):
        self.emit('is-setup')
        
    def set_user_stylesheet(self, uri):
        settings = self.get_settings()

        if os.path.exists(uri):
            # used to disable flash movies until you click them.
            settings.set_property('user-stylesheet-uri', 'file:///' + uri)
    
    def set_agent_stylesheet(self, uri):
        self.set_user_stylesheet(uri)