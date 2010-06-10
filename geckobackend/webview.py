import logging

import gobject

import xpcom
from xpcom.nsError import *
from xpcom import components
from xpcom.components import interfaces

import hulahop
from hulahop.webview import WebView as GeckoWebView

from sugar import env

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
        
        # enable typeahead
        cls = components.classes["@mozilla.org/typeaheadfind;1"]
        self.typeahead = cls.createInstance(interfaces.nsITypeAheadFind)
        
        # don't pick up the sugar theme - use the native mozilla one instead
        cls = components.classes['@mozilla.org/preferences-service;1']
        pref_service = cls.getService(components.interfaces.nsIPrefService)
        branch = pref_service.getBranch("mozilla.widget.")
        branch.setBoolPref("disable-native-theme", True)
        
    def do_setup(self):
        WebView.do_setup(self)

        listener = xpcom.server.WrapObject(ContentInvoker(self),
                                           interfaces.nsIDOMEventListener)
        self.window_root.addEventListener('click', listener, False)

        listener = xpcom.server.WrapObject(CommandListener(self.dom_window),
                                           interfaces.nsIDOMEventListener)
        self.window_root.addEventListener('command', listener, False)

        #self.progress.setup(self)
        #self.history.setup(self.web_navigation)

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
            
    def set_user_stylesheet(self, uri):
        io_service2 = io_service_class.getService(interfaces.nsIIOService2)
        io_service2.manageOfflineStatus = False

        cls = components.classes['@mozilla.org/content/style-sheet-service;1']
        style_sheet_service = cls.getService(interfaces.nsIStyleSheetService)

        if os.path.exists(uri):
            user_sheet_uri = io_service.newURI('file:///' + uri, None, None)
            style_sheet_service.loadAndRegisterSheet(user_sheet_uri,
                    interfaces.nsIStyleSheetService.USER_SHEET)
    
    def set_agent_stylesheet(self, uri):
        io_service2 = io_service_class.getService(interfaces.nsIIOService2)
        io_service2.manageOfflineStatus = False

        cls = components.classes['@mozilla.org/content/style-sheet-service;1']
        style_sheet_service = cls.getService(interfaces.nsIStyleSheetService)

        if os.path.exists(uri):
            agent_sheet_uri = io_service.newURI('file:///' + uri, None, None)
            style_sheet_service.loadAndRegisterSheet(agent_sheet_uri,
                    interfaces.nsIStyleSheetService.AGENT_SHEET)