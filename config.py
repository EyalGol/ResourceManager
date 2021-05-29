PORT = 5555
DEBUG = True
SECRET_KEY = 'CHANGE_ME'
AUTH = 'NO_AUTH'

DB_PATH = 'db.sql'

# Setup LDAP Configuration Variables. Change these to your own settings.
# All configuration directives can be found in the documentation.
LDAP_CONFIG = dict()

# Hostname of your LDAP Server
LDAP_CONFIG['LDAP_HOST'] = 'ad.mydomain.com'

# Base DN of your directory
LDAP_CONFIG['LDAP_BASE_DN'] = 'dc=mydomain,dc=com'

# Users DN to be prepended to the Base DN
LDAP_CONFIG['LDAP_USER_DN'] = 'ou=users'

# Groups DN to be prepended to the Base DN
LDAP_CONFIG['LDAP_GROUP_DN'] = 'ou=groups'

# The RDN attribute for your user schema on LDAP
LDAP_CONFIG['LDAP_USER_RDN_ATTR'] = 'cn'

# The Attribute you want users to authenticate to LDAP with.
LDAP_CONFIG['LDAP_USER_LOGIN_ATTR'] = 'mail'

# The Username to bind to LDAP with
LDAP_CONFIG['LDAP_BIND_USER_DN'] = None

# The Password to bind to LDAP with
LDAP_CONFIG['LDAP_BIND_USER_PASSWORD'] = None
