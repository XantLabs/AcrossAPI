"""Map URLs to view functions. Allows more modular code."""

import views

# Note that all will be POST requests.
URLS = [
    ('/api/upload', views.upload),
    ('/media/<filename>', views.uploadedFile),
]
