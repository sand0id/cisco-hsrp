HSRP Getter

Shows the HSRP status of a device pair. Call the app on `/` with the following:

```
{
    "devices": [
        {
            "name": "CE1",
            "managementIP": "1.1.1.1"
            
        },
        {
            "name": "CE2",
            "managementIP": "1.1.1.2"
            
        }
    ]
}
```

It calls `show standby brief` on each device. It then looks for the `Priority` and `Active` state on each device's HSRP groups. 
If the device's group has a higher priority than it's partner, and the group is `Active`, it's a pass. Otherwise, it will show the error. 

Example outputs below

Good result:
```
{
    "hsrp_result": [
        {
            "CE1": [
                {
                    "group": "Group 1",
                    "status": "Pass"
                },
                {
                    "group": "Group 2",
                    "status": "Pass"
                }
            ]
        },
        {
            "CE2": [
                {
                    "group": "Group 1",
                    "status": "Pass"
                },
                {
                    "group": "Group 2",
                    "status": "Pass"
                }
            ]
        }
    ]
}
```

Bad result:
```
{
    "hsrp_result": [
        {
            "CE1": [
                {
                    "group": "Group 1",
                    "status": "Pass"
                },
                {
                    "group": "Group 2",
                    "status": "Fail - No longer Active"
                }
            ]
        },
        {
            "CE2": [
                {
                    "group": "Group 1",
                    "status": "Pass"
                },
                {
                    "group": "Group 2",
                    "status": "Fail - No longer Standby"
                }
            ]
        }
    ]
}
```
