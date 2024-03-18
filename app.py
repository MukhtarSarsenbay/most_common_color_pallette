from flask import Flask, request, render_template_string
from PIL import Image
from collections import Counter
import io

app = Flask(__name__)

HTML = """
<!doctype html>
<title>Upload an Image</title>
<h1>Upload an image to find its most common colors</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Upload>
</form>
{% if colors %}
  <ul>
  {% for color in colors %}
    <li style="background:{{ color }};color:{{ color }}">Color: {{ color }}</li>
  {% endfor %}
  </ul>
{% endif %}
"""

def get_most_common_colors(image, n_colors=5):
    image = image.convert('RGB')
    result = Counter(image.getdata())
    most_common = result.most_common(n_colors)
    colors = ['#%02x%02x%02x' % (r, g, b) for (r, g, b), count in most_common]
    return colors

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            image = Image.open(io.BytesIO(file.read()))
            colors = get_most_common_colors(image)
            return render_template_string(HTML, colors=colors)
    return render_template_string(HTML, colors=None)

if __name__ == '__main__':
    app.run(debug=True)
