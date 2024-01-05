#!/usr/bin/env python3
from flask import Flask, render_template
from routes import blueprint  # Import the blueprint from routes.py

app = Flask(__name__)
app.register_blueprint(blueprint)  # Register the blueprint

@app.route('/')
def index():
    # Render the HTML file for image upload
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)