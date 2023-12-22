import os
from flask import Flask, request
from dotenv import load_dotenv

from core.device import Device
from core.credentials import Credentials
app = Flask(__name__)


@app.route('/', methods=['POST'])
def home():
    # Get input from HTTP Post request (not doing error handling for now)
    request_data = request.get_json()

    # Load credentials from .env
    device_creds = Credentials(
        os.getenv('DEVICE_USERNAME'), os.getenv('DEVICE_PASSWORD'))

    # Create devices
    devices = []
    if len(request_data['devices']) is not 2:
        raise ValueError("Must be exactly two devices")

    for request_device in request_data['devices']:

        # Create a device from the input data
        template = open('./templates/cisco_show_standby_brief.textfsm', 'r', encoding="UTF-8")
        device = Device(
            request_device['name'],
            request_device['managementIP'],
            device_creds,
            template)

        # Get the HSRP data
        device.get_hsrp_data()

        # Add the device
        devices.append(device)
    
    # For each device, pass in the partner device's hsrp groups
    # This allows us to compare priority
    devices[0].inspect_partner(devices[1].hsrp_groups)
    devices[1].inspect_partner(devices[0].hsrp_groups)

    # Get the result to display
    device_output = []
    to_print = {
        "hsrp_result": device_output
    }
    for device in devices:
        device_output.append(device.print_hsrp())

    return to_print



if __name__ == '__main__':
    load_dotenv()
    app.run()
