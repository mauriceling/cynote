"""
This line is needed to let CyNote knows this plugin is installed.

Format: session.installed_plugins[('<module name>', 
                                   '<entry function>')] = '<short name>'
                                   
The link on the header tab will then be
http://<host>:<port>/<application name>/<module name>/<entry function>
"""
# session.installed_plugins[('plugin_template', 'index')] = 'A template'