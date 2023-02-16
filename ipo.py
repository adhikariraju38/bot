import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

BOT_TOKEN = '5639755535:AAFWlHOyhBANI0u-6GFHspbkP4h5E-aBoxY'
CHAT_ID = '5891316395'

def send_photo(photo, caption=None):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'

    files = {'photo': ('pic.jpg', photo)}
    data = {'chat_id': CHAT_ID}
    if caption:
        data['caption'] = caption

    r = requests.post(url, files=files, data=data)
    return r.json()

def file_url(file_id):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}'
    r=requests.post(url)
    return r.json()

# Create Flask app
app = Flask(__name__, template_folder='.')
CORS(app)


@app.route('/imgurl', methods=['POST'])
def predict():
    # Get the image file from the request
    file = request.files['image'].read()
    response = send_photo(file, "Photo being uploaded from ICTC")
    file_id = response["result"]["photo"][-1]["file_id"]
    fileUrl=file_url(file_id)
    final_url=fileUrl["result"]["file_path"]
    image_url="https://api.telegram.org/file/bot"+BOT_TOKEN+"/"+final_url
    return jsonify(image_url=image_url)


if __name__ == '__main__':
    app.run(debug=True)
