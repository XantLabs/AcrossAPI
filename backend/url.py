"""Map URLs to view functions. Allows more modular code."""

import views

# Note that all will/must be POST requests.
URLS = [
    ('/api/upload', views.upload, "POST"),
    ('/api/media/<filename>', views.uploadedFile, "GET"),
    ('/api/getmedia', views.sendTopPhotos, "POST"),
]

test = "test"
