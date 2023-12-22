class HsrpGroup:

    def __init__(self, device_name, group_id: int, priority: int, active: bool):
        self.device_name = device_name
        self.group_id = group_id
        self.priority = priority
        self.active = active
        self.partner_priority = 0

    def set_partner_priority(self, partner_priority:int):
        self.partner_priority = partner_priority

    def print_hsrp(self) -> dict:
        group_string = f"Group {self.group_id}"
        status_string = "Pass"
        if self.priority > self.partner_priority and not self.active:
            status_string = "Fail - No longer Active"
        if self.priority < self.partner_priority and self.active:
            status_string = "Fail - No longer Standby"

        return {
            "group" : group_string,
            "status" : status_string
        }




