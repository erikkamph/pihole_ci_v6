class HoleException(Exception):
    """Raised when there's an error with the pi-hole instance communication"""

class HoleVersionError(Exception):
    """Raise when there is an issue with the version of the integration either installed or released"""