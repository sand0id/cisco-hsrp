from core.device import Device

class Collector:
    # Could be some setup needed here, if this class were to do more
    def __init__(self):
        pass

    # Just print what we need...
    def get_hsrp_info(self, devices):
        result_devices = []
        result = {
            "hsrp_result": result_devices
        }
        device: Device
        for device in devices:
            result_devices.append({
                device.name : device.get_formatted_hsrp_result()
            })
        return result


        

    