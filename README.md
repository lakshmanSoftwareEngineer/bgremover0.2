# Background Remover API

A Flask API service that removes backgrounds from images using AI.

## Features

- Upload images and get background-removed versions
- RESTful API with binary image support
- CORS enabled for web applications
- Error handling and logging
- Production-ready for deployment

## API Endpoints

### Health Check

```
GET /
```

Returns service status.

### Remove Background

```
POST /upload
Content-Type: application/octet-stream
Body: Binary image data
```

Returns processed image with background removed.

## Usage

### With curl:

```bash
curl -X POST https://your-app.onrender.com/upload \
     --header "Content-Type: application/octet-stream" \
     --data-binary "@your-image.jpg" \
     --output result.png
```

### With Python requests:

```python
import requests

with open('image.jpg', 'rb') as f:
    response = requests.post(
        'https://your-app.onrender.com/upload',
        data=f.read(),
        headers={'Content-Type': 'application/octet-stream'}
    )

with open('output.png', 'wb') as f:
    f.write(response.content)
```

## Deployment

This app is configured for deployment on Render.com with:

- Gunicorn WSGI server
- Environment-based configuration
- Health check endpoint
- Error handling and logging
