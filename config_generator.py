import json
from pathlib import Path

interface_template = """!
interface {interface}
 ip address {address}
exit"""

ip_route_template = 'ip route {from_addr} {to} {interface}'

ffr_cfg_template = """!
frr version 8.4_git
frr defaults traditional
hostname {hostname}
no ipv6 forwarding
{interfaces}
{routes}
!
end"""

file_cfg = Path('in/config.json')
file_content = file_cfg.read_text()
config = json.loads(file_content)

nodes_cfg = config['nodes']

for (key, node_cfg) in nodes_cfg.items():
    node_path = Path(key)
    node_path.mkdir(parents=True, exist_ok=True)

    hostname = node_cfg['hostname']

    interfaces = []
    interfaces_cfg = node_cfg['interfaces']

    for (interface, interface_cfg) in interfaces_cfg.items():
        address = '{ip}/{mask}'.format(
            ip=interface_cfg['ip'],
            mask=interface_cfg['mask']
        )
        interfaces.append(
            interface_template.format(
                interface=interface,
                address=address
            )
        )

    routes = []
    routes_cfg = node_cfg['routes']

    for route_cfg in routes_cfg:
        if len(routes) == 0:
            routes.append('!')

        routes.append(
            ip_route_template.format(
                from_addr=route_cfg['from'],
                to=route_cfg['to'],
                interface=route_cfg['interface']
            )
        )

    ffr_cfg = ffr_cfg_template.format(
        hostname=hostname,
        interfaces='\n'.join(interfaces),
        routes='\n'.join(routes)
    )

    ffr_file = Path('ffr_{node}.conf'.format(node=key))
    ffr_file.write_text(ffr_cfg)
