import docker
from docker.models.containers import Container


def remove_garbage(text: str, garbage: str) -> str:
    garbage_index = text.index(garbage)
    if garbage_index < 0:
        return text
    garbage_index += len(garbage)
    return text[garbage_index:]


def run_pretty_print(output: str):
    print("Device config:")
    print(remove_garbage(output, 'Current configuration:'))


def run_ip_routes(output: str):
    print("Device IP routes:")
    print(remove_garbage(output, "'No such file or directory'."))


def run_int_brief(output: str):
    print("Short interfaces description:")
    print(remove_garbage(output, "'No such file or directory'."))


def run_ip_route(output: str):
    print("Short interface description:")
    print(remove_garbage(output, "'No such file or directory'."))


def run_ping(output: str):
    if output != "" and "bytes from" not in output:
        print(output)


commands = {
    "run": {
        "executor": "vtysh",
        "command": "sh run",
        "handler": run_pretty_print
    },
    "routes": {
        "executor": "vtysh",
        "command": "sh ip route",
        "handler": run_ip_routes
    },
    "brief": {
        "executor": "vtysh",
        "command": "sh int brief",
        "handler": run_int_brief
    },
    "route": {
        "executor": "vtysh",
        "command": "show ip route {ip}",
        "inputs": [
            {
                "placeholder": "ip",
                "text": "Input IP: "
            }
        ],
        "handler": run_ip_route
    },
    "ping": {
        "executor": "sh",
        "command": "ping -c 10 -W 1 {ip}",
        "inputs": [
            {
                "placeholder": "ip",
                "text": "Input IP: "
            }
        ],
        "handler": run_ping
    },
    "traceroute": {
        "executor": "sh",
        "command": "traceroute -m 10 {ip}",
        "inputs": [
            {
                "placeholder": "ip",
                "text": "Input IP: "
            }
        ],
        "handler": print
    }
}


def node_commands(device_container: Container, command):
    executor = command['executor']
    cmd = command['command']
    if 'inputs' in command:
        placeholders = dict()
        inputs = command['inputs']
        for input_cfg in inputs:
            placeholders[input_cfg['placeholder']] = input(input_cfg['text'])
        cmd = cmd.format(**placeholders)

    handler = command['handler']
    print(f"Execute command: {cmd}")
    _, stream = device_container.exec_run(f'{executor} -c "{cmd}"', stream=True)
    for data in stream:
        for line in data.decode('utf-8').split('\n'):
            handler(line)


if __name__ == "__main__":
    container_id = input("Input container id or name: ")
    command_type = input("Input command: ")

    if command_type not in commands:
        raise ValueError('Unknown command_type')

    command = commands[command_type]

    docker_client = docker.from_env()
    device_container = docker_client.containers.get(container_id)

    print(f"Container: {device_container.name}")
    node_commands(device_container, command)
