from io import BytesIO
from flask import Flask, request, send_file, jsonify
from rembg import remove
from PIL import Image

# ====== KONFIG ======
MAX_UPLOAD_MB = 20
TARGET_BYTES_DEFAULT = 1_000_000  # 1 MB
MAX_SIDE_DEFAULT = 1600
STEP_SHRINK = 0.85
MIN_SIDE = 300

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_MB * 1024 * 1024


@app.post("/api/removebg")
def remove_background():
    file = request.files.get("image")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    try:
        img = Image.open(file.stream)
        # Hapus background
        output = remove(img).convert("RGBA")

        # Simpan ke memory buffer
        buf = BytesIO()
        output.save(buf, format="PNG", optimize=True)
        buf.seek(0)

        # Kembalikan langsung sebagai file PNG
        return send_file(buf, mimetype="image/png", as_attachment=False)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get("/")
def home():
    return """
    <h2>🖼️ Remove Background API</h2>
    <form action="/api/removebg" method="post" enctype="multipart/form-data">
      <input type="file" name="image" accept="image/*" required>
      <button type="submit">Upload</button>
    </form>
    <p>Gunakan endpoint POST /api/removebg (multipart/form-data)</p>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
