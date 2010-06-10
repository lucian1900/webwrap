#!/usr/bin/env python

import logging

try:
    from geckobackend import *
    from geckobackend import webview
except ImportError, e:
    logging.debug(e)
    logging.warning('hulahop could not be loaded, trying pywebkitgtk.')
    
    try:
        from webkitbackend import *
        from webkitbackend import webview
    except ImportError:
        logging.error('pywebkitgtk could not be loaded. No suitable web engine \
                      found')
    else:
        logging.info("Using pywebkitgtk")
else:
    logging.info("Using hulahop")

if __name__ == '__main__':
    import gtk
    
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.set_size_request(800,600)
    win.connect('destroy', gtk.main_quit)
    wv = webview.WebView()
    wv.load_uri('http://google.com')
    wv.show()
    
    win.add(wv)
    
    win.show()
    gtk.main()