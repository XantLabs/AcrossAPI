"""Provide views bound to urls. Does not include error handlers."""


def index():
    """Handle requests to root URL. Return 403."""
    return "200, but will be 403 later."
