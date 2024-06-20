from flask import Flask, request, send_file, jsonify
import sqlite3
import numpy as np
from PIL import Image
import io
from processImage import applyCustomColormap
import initializeDB
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/')
def home():
    return "Database initialized successfully!"

@app.route('/image_frames', methods=['GET'])
def get_image_frames():
    """
    Retrieve image frames based on depth values.
    ---
    parameters:
      - name: depth_min
        in: query
        type: integer
        required: true
        description: Minimum depth value.
        default: 9000
      - name: depth_max
        in: query
        type: integer
        required: true
        description: Maximum depth value.
        default: 9010
    responses:
      200:
        description: A PNG image of the combined frames.
        content:
          image/png:
            schema:
              type: string
              format: binary
      404:
        description: No frames found for the given depth range.
    """
    try:
        depth_min = int(request.args.get('depth_min'))
        depth_max = int(request.args.get('depth_max'))

        print(f"Querying for depths between {depth_min} and {depth_max}")

        conn = sqlite3.connect('images.db')
        c = conn.cursor()
        c.execute('SELECT * FROM image_frames WHERE depth BETWEEN ? AND ?', (depth_min, depth_max))
        rows = c.fetchall()
        conn.close()

        if not rows:
            print("No frames found for the given depth range")
            return "No frames found for the given depth range", 404

        frames = []
        for row in rows:
            depth, pixel_data = row
            print(f"Processing depth: {depth}")
            image_array = np.frombuffer(pixel_data, dtype=np.uint8).reshape(-1, 150)
            colored_image = applyCustomColormap(image_array)
            frames.append((depth, colored_image))

        combined_image = np.vstack([frame[1] for frame in frames])
        im = Image.fromarray(combined_image)

        buf = io.BytesIO()
        im.save(buf, format='PNG')
        buf.seek(0)

        return send_file(buf, mimetype='image/png')

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    try:
        initializeDB.initialize_database('img.csv')
        print("Database initialized.")
    except Exception as e:
        print(f"Error initializing database: {e}")
    app.run(host='0.0.0.0', port=3000)
    app.config['SWAGGER'] = {
    'title': 'Image Frames API',
    'uiversion': 3
}
