from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Replace this with your actual authorization token
AUTH_TOKEN = "AQEAxpweCiWv0QCmmVTefl0TDnDY1107Fqirpgoe3xJL8CvFko+3"

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/get_devices', methods=['POST'])
def get_devices():
    cnt = request.form.get('count')  # Number of devices to retrieve
    deveui = request.form.get('deveui')  # Optional: starting point for the list

    # Call the API to get the list of devices
    headers = {'Authorization': AUTH_TOKEN}
    data = {"cnt": int(cnt)}
    if deveui:
        data['deveui'] = deveui

    response = requests.post('https://mgs.loracloud.com/api/v1/device/list', headers=headers, json=data)
    device_list = response.json().get('result', [])

    return render_template('index.html', devices=device_list)

@app.route('/get_device_info', methods=['POST'])
def get_device_info():
    selected_devices = request.form.getlist('selected_devices[]')

    # Call the API to get device info for the selected devices
    headers = {'Authorization': AUTH_TOKEN}
    data = {"deveuis": selected_devices}

    response = requests.post('https://mgs.loracloud.com/api/v1/device/info', headers=headers, json=data)
    device_info = response.json()

    return jsonify(device_info)

if __name__ == '__main__':
    app.run(debug=True)
