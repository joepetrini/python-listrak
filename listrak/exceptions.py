

class ProhibitedIPAddressException(Exception):
    """IP address prohibited.  You need to add the traklis IP address to your authorized API list."""

class InvalidLogonAttempt(Exception):
    """Invalid user name or password."""
    