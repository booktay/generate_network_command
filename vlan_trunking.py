def generate_uplink_port_channal(devices):
    for device in devices:
        print("show interface description | include " + device)

def generate_interface_status(interface_name):
    prefix = "M::C["
    interface_name = interface_name.upper()
    interface_name = interface_name.split(", ")
    interface_all = [''.join(set(s)) for s in zip(*interface_name)]
    print("show interface status | include M::C[" + "][".join(interface_all[1:])+ "]")
    for name in interface_name:
        print("! " + name)

def generate_interface_vlan(vlans):
    print("show running-config interface vlan " + ", vlan ".join(vlans))

def generate_vlan(vlans):
    print("show vlan id " + ", ".join(vlans))
    print("show running-config vlan " + ", ".join(vlans))

def generate_uplink_inteface(uplink_po):
    print("show running-config interface port-channel " + ", port-channel ".join(uplink_po))

def generate_uplink_trunk_inteface(uplink_po):
    print("show interface port-channel " + ", ".join(uplink_po) + " trunk")

def generate_downlink_interface(downlink_po, uplink_po):
    print("show running-config interface port-channel " + ", port-channel ".join(downlink_po) + ", port-channel " + uplink_po)

def generate_add_or_remove_vlans(vlans, command):
    print("switchport trunk allowed vlan " + command + " " + ", ".join(vlans))

def generate_uplink_command(uplink, downlink):
    swas = []
    vlans = []
    uplink_po = []
    for data in downlink:
        swas.append(data[0].upper())
        vlans += data[1]
        uplink_po.append(data[3])

    vlans_id = [v.split(' ')[0] for v in vlans]
    vlans_id = set(vlans_id)

    print("! On " + uplink.upper() + "1/2:")
    print("show logging")
    print("terminal length 0")
    generate_uplink_port_channal(swas)
    generate_interface_vlan(vlans_id)
    generate_vlan(vlans_id)
    generate_uplink_trunk_inteface(uplink_po)
    generate_uplink_inteface(uplink_po)
    print("configure terminal")
    for detail in downlink:
        print("interface port-channel " + detail[3])
        generate_add_or_remove_vlans([v.split(' ')[0] for v in detail[1]], "add")
    print("end")
    print("copy running-config startup-config")
    generate_vlan(vlans_id)
    generate_uplink_trunk_inteface(uplink_po)
    generate_uplink_inteface(uplink_po)
    print("show logging")
    print("! " + "="*60)
    print("configure terminal")
    for detail in downlink:
        print("interface port-channel " + detail[3])
        generate_add_or_remove_vlans([v.split(' ')[0] for v in detail[1]], "remove")
    print("end")
    print("copy running-config startup-config")
    print("!")

def generate_downlink_command(uplink, downlink):
    for detail in downlink:
        print("! On " + detail[0].upper() + "1/2:")
        print("show logging")
        print("terminal length 0")
        generate_uplink_port_channal([uplink.upper()])
        generate_interface_status(detail[2])
        vlans_id = [v.split(' ')[0] for v in detail[1]]
        vlans_name = [v.split(' ')[1] for v in detail[1]]
        generate_vlan(vlans_id)
        generate_uplink_trunk_inteface([detail[3]])
        generate_downlink_interface(detail[4].split(', '), detail[3])
        print("configure terminal")
        for index, vlan_id in enumerate(vlans_id):
            print("vlan " + vlan_id)
            print("name " + vlans_name[index])
        print("interface port-channel " + ", port-channel ".join(detail[4].split(', ')) + ", port-channel " + detail[3])
        generate_add_or_remove_vlans(vlans_id, "add")
        print("end")
        print("copy running-config startup-config")
        generate_vlan(vlans_id)
        generate_uplink_trunk_inteface([detail[3]])
        generate_downlink_interface(detail[4].split(', '), detail[3])
        generate_interface_status(detail[2])
        print("show logging")
        print("! " + "="*60)
        print("configure terminal")
        print("interface port-channel " + ", port-channel ".join(detail[4].split(', ')) + ", port-channel " + detail[3])
        generate_add_or_remove_vlans(vlans_id, "remove")
        print("exit")
        for index, vlan_id in enumerate(vlans_id):
            print("no vlan " + vlan_id)
        print("end")
        print("copy running-config startup-config")
        print("!")

def input_data():
    # Example Format
    #     uplink = "aaa-example-rta"
    #     downlink = [
    #         [
    #             "abc-example-swa",
    #             [
    #                 "1261 SITE-A",
    #                 "1262 SITE-B"
    #             ],
    #             "c949xvz, C417cbh, C821ezk, C425sfe, C357jxn, C754ztt, C898ebb, C648jgt",
    #             "1727",
    #             "13-16, 18-21"
    #         ],
    #         [
    #             "def-example-swa",
    #             [
    #                 "1261 SITE-A",
    #                 "1263 SITE-C"
    #             ],
    #             "c725ynz, C490dgs, C340ndu, C005ats, C594jry, C827pxr, C704jrd, C726dcz, C735qwr, C767bsh, C750xcf, C409tqv, C390spa, C377rfd, C831bmj, C686vjn",
    #             "1728",
    #             "1-17"
    #         ]
    #     ]

    uplink = ""
    downlink = [
        [
            "",
            [
                "",
                ""
            ],
            "",
            "",
            ""
        ]
    ]
    return uplink, downlink

if __name__ == "__main__":
    uplink, downlink = input_data()
    print(">>> Generate Command >>>")
    print(">>>" + "="*60 +">>>")
    generate_uplink_command(uplink, downlink)
    generate_downlink_command(uplink, downlink)
    print(">>>" + "="*60 +">>>")
    