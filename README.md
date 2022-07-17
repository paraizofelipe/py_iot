### py_iot

### Commands

Install all project dependencies

```bash
$ poetry install
```

Run the configuration process, using the keys, token and IP from the tuya project

```bash
$ cd ./setup
$ poetry run python -m tinytuya wizard 
```

With all the configuration JSON files pulling from the environment. Scan the network to find all tuya devices on the network
**Note:** This process is necessary to get the **local_keys** of the devices

```bash
$ poetry run python -m tinytuya scan
```

Command to collect status of device named Lamp

```bash
$ poetry run local_iot show_status Lamp
```

Command to turn the device on and off

```bash
$ poetry run local_iot switch Lamp 
```

Command to modify the RGB device color

Supported colors: red, orange, yellow, green, blue, indigo, violet, turquoise, magenta and white

```bash
$ poetry run local_iot color Lamp red
```
