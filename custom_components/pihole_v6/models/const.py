from datetime import timedelta

DOMAIN="pihole_v6"

DEFAULT_HOST = "pi.hole"
DEFAULT_LOCATION = "api"
DEFAULT_PORT = 80
DEFAULT_VERIFY_SSL = False
DEFAULT_API_KEY = ""
DEFAULT_NAME = "pihole"

SERVICE_DISABLE = "disable"
SERVICE_DISABLE_ATTR_DURATION = "duration"

CONF_SID = "sid"
CONF_CSRF = "csrf"
CONF_SCHEMA = "scheme"

HEADER_SID = "X-FTL-SID"
HEADER_CSRF = "X-FTL-CSRF"

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)