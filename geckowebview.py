import os
import logging

from sugar import env

import xpcom
from xpcom.nsError import *
from xpcom import components
from xpcom.components import interfaces

import hulahop
from hulahop.webview import WebView as GeckoWebView

hulahop.startup(os.path.join(env.get_profile_path(), 'gecko'))

class WebView(GeckoWebView):
    __gtype_name__ = 'WebView'
    __gsignals__ = {
        'is-setup': (gobject.SIGNAL_RUN_FIRST,
                  gobject.TYPE_NONE,
                  ([]))
    }
    
    _com_interfaces_ = interfaces.nsIWindowCreator
    
    def __init__(self):
        GeckoWebView.__init__(self)
        
        io_service_class = components.classes[ \
                "@mozilla.org/network/io-service;1"]
        io_service = io_service_class.getService(interfaces.nsIIOService)

        # Use xpcom to turn off "offline mode" detection, which disables
        # access to localhost for no good reason.  (Trac #6250.)
        io_service2 = io_service_class.getService(interfaces.nsIIOService2)
        io_service2.manageOfflineStatus = False
        
        cls = components.classes["@mozilla.org/typeaheadfind;1"]
        self.typeahead = cls.createInstance(interfaces.nsITypeAheadFind)
        
    def do_setup(self):
        WebView.do_setup(self)

        listener = xpcom.server.WrapObject(ContentInvoker(self),
                                           interfaces.nsIDOMEventListener)
        self.window_root.addEventListener('click', listener, False)

        listener = xpcom.server.WrapObject(CommandListener(self.dom_window),
                                           interfaces.nsIDOMEventListener)
        self.window_root.addEventListener('command', listener, False)

        self.progress.setup(self)
        self.history.setup(self.web_navigation)

        self.typeahead.init(self.doc_shell)

        self.emit('is-setup')
        
    def zoom_in(self):
        contentViewer = self.doc_shell.queryInterface( \
                interfaces.nsIDocShell).contentViewer
        if contentViewer is not None:
            markupDocumentViewer = contentViewer.queryInterface( \
                    interfaces.nsIMarkupDocumentViewer)
            markupDocumentViewer.fullZoom += _ZOOM_AMOUNT

    def zoom_out(self):
        contentViewer = self.doc_shell.queryInterface( \
                interfaces.nsIDocShell).contentViewer
        if contentViewer is not None:
            markupDocumentViewer = contentViewer.queryInterface( \
                    interfaces.nsIMarkupDocumentViewer)
            markupDocumentViewer.fullZoom -= _ZOOM_AMOUNT