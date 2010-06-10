def set_locale(lang):
    cls = components.classes["@mozilla.org/preferences-service;1"]
    prefService = cls.getService(components.interfaces.nsIPrefService)
    branch = prefService.getBranch('')
    branch.setCharPref('intl.accept_languages', lang)
    
def set_profile_path(path):
    hulahop.startup(path)
    
def set_app_version(version):
    hulahop.set_app_version(version)