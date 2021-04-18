# smart room - controller

Smart Room Controller

As a controller of A/C, controller.py create a multi-thread socket server to receive control command.

Main API Server will create a socket connection to controller and send payload for controlling A/C.

In our case, controller is running on a Raspberry Pi Zero W.

## Payload

Socket transfer data type in bytes, the data structure above need to transfer (or encode) to bytes.

### Format

JSON string containing Python Dict object
+ token: controller token
    + 32 bytes random number in hex
    + eg. `e8b4ac80acc520ae59686b1c3715281ede9b61c547407a9c90371f1cb5dfeac2`
+ command: A/C command
    + set temperature or turn off
    + eg. `25C`, `off`

### emample

```json
{
    "token": "TOKEN",
    "command": "25C"
}
```

## Getting Started

### Prerequisites

- python 3.7
- pip3

### Running Development

Installing Packages & Running
```sh
pip3 install -r requirements.txt
python3 controller.py
```

### Testing Command

+  Test Connection Using `nc`
    `$ nc [hostname] [port] <<< '{"token":"TOKEN","command":"25C"}'`
