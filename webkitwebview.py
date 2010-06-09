#!/usr/bin/env python

from webkit import WebView as WebkitWebView

class WebView(WebkitWebView):
    __gtype_name__ = "WebView"
    
    def __init__(self):
        WebkitWebView.__init__(self)
        
        self.set_full_content_zoom(True)