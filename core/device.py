import textfsm
from core.credentials import Credentials
from core.hsrpgroup import HsrpGroup


class Device:

    # Device config defined statically for now, this would be via SSH CLI
    # You can edit the response here. Ideally move to unit test
    # There is some guff at the start of each line, but textfsm seems to cope
    deviceConfig= {
        "1.1.1.1" : 
"""                     P indicates configured to preempt.
                     |
Interface   Grp  Pri P State   Active          Standby         Virtual IP
Gi0/0/1     1    110 P Active  local           82.0.0.3        82.0.0.1
Gi0/0/1     2    115 P Standby 82.0.0.11       local           82.0.0.9""",
        "1.1.1.2" : 
"""                     P indicates configured to preempt.
                     |
Interface   Grp  Pri P State   Active          Standby         Virtual IP
Gi0/0/1     1    105 P Standby 82.0.0.2        local           82.0.0.1
Gi0/0/1     2    110 P Active  local           82.0.0.10       82.0.0.9"""
    }

    def __init__(self, name, management_ip, credentials: Credentials, text_fsm_template):
        self.name = name
        self.management_ip = management_ip
        self.credentials = credentials
        self.fsm = textfsm.TextFSM(text_fsm_template)
        self.hsrp_groups = []

    # Get the HSRP data for this device using textfsm
    def get_hsrp_data(self):

        # Parse the command output
        # Pretend we are going to the device via it's IP
        result = self.fsm.ParseText(self.deviceConfig[self.management_ip])

        # Get the data out
        grouprows = [dict(zip(self.fsm.header, entry)) for entry in result]

        # Loop through the returned group rows and create hsrp groups for this device
        for grouprow in grouprows:
            group_id = int(grouprow['GROUP'])
            group_priority = int(grouprow['PRIORITY'])
            group_active = True if grouprow['STATE'] == "Active" else False
            self.hsrp_groups.append(HsrpGroup(self.name, group_id, group_priority, group_active))
    
    # Pass in the partner hsrp groups, so we can see the priority
    def inspect_partner(self, partner_hsrp_groups):

        # Find matching groups and set the partner priority
        for this_hsrp_group in self.hsrp_groups:
            for partner_hsrp_group in partner_hsrp_groups:
                if this_hsrp_group.group_id == partner_hsrp_group.group_id:
                    # Let this hsrp group know the priority of it's partner
                    this_hsrp_group.set_partner_priority(partner_hsrp_group.priority)

    # Get the result in a format suitable for printing
    def print_hsrp(self) -> dict:
        hsrp_result = []
        for hsrp_group in self.hsrp_groups:
            hsrp_result.append(hsrp_group.print_hsrp())
        return {
            self.name: hsrp_result
        }
            

    


