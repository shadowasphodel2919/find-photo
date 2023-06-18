from flask import Flask, render_template, request, jsonify
from api import *
from PIL import Image
import base64

app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')

@app.route('/', methods =["GET", "POST"])
def index():
    if request.method == "POST" and 'get_link' in request.form:
        link = request.form.get("link")
        faces = request.files['image']
        print(type(faces))
        found_pictures, count = search_photos(faces, link)
        print(found_pictures)
        print(count)
        return render_template("index.html", count = count, pics = found_pictures)
    else:
        return render_template("index.html")


if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)