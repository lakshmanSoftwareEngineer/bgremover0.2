from flask import Flask, request, send_file
import io
import os
from PIL import Image
import rembg
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration for Render
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

@app.route('/', methods=['GET', 'HEAD'])
def health_check():
    """Health check endpoint"""
    return 'OK', 200

@app.route('/health', methods=['GET'])
def health_status():
    """Detailed health status"""
    return {'status': 'healthy', 'service': 'background-remover', 'message': 'POST image to /upload endpoint'}, 200

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            return 'No image uploaded', 400
        file = request.files['image']
        try:
            input_image = Image.open(file.stream)
        except Exception as e:
            return f"Invalid image file: {e}", 400
        output_image = rembg.remove(input_image)
        output_image.save("output.png")
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return {'error': 'File too large. Maximum size is 16MB'}, 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return {'error': 'Endpoint not found'}, 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {e}")
    return {'error': 'Internal server error'}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

