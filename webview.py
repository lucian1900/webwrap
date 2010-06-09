#!/usr/bin/env python

try:
    from hulahop.webview import WebView as BackendWebView
except ImportError:
    from webview import WebView as BackendWebView
    
class WebView(BackendWebView):
    pass

if __name__ == '__main__':
    import gtk
    
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.set_size_request(800,600)
    win.connect('destroy', gtk.main_quit)
    wv = WebView()
    wv.load_uri('http://google.com')
    wv.show()
    
    win.add(wv)
    
    win.show()
    gtk.main()