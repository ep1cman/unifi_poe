# Intro
This is a small command-line tool to control the state of Power over Ethernet 
(PoE) ports on Ubiquiti Networks switches being controlled by a Unifi
controller. It allows you to turn PoE ports on, off, and power cycles them.

If you encounter any issues, please open an issue on the GitHub repo. Pull
requests for any improvements are always welcome.

If you like this software and want to support me and my work, you can:

[![Buy me a coffee](https://www.buymeacoffee.com/assets/img/custom_images/black_img.png)](https://www.buymeacoffee.com/ep1cman)

# Setup

1. Either perform a git clone of this repository or use the "Download ZIP"
option in the "Code" drop-down menu above.
2. Open a terminal and navigate to where you cloned/download the repository.
3. Run `pip install .`
4. Before this tool will work, you need to log into the Unifi controller web UI 
and populate the API with default values for the port. This can be done as follows:
    1. Go to the "Devices" tab.
    2. Click on the switch you want to control.
    3. In the side menu that opens up click on the ports tab.
    4. Find the port you want to control and click the edit (pencil) icon.
    5. Expand the "Profile overrides" menu.
    6. Make any change here, click apply, then revert it back and apply again. 

# Usage
```
Usage: unifi_poe [OPTIONS] COMMAND [ARGS]...

  Control the state of port SWITCH_PORT on Unifi switch SWITCH_MAC_ADDRESS

Options:
  --host TEXT                     The URL of the unifi controller  [required]
  --username TEXT                 username to access the unifi api  [required]
  --password TEXT                 password to access the unifi api
  --controller_type [udm|unifi_controller]
                                  Unifi controller type
  -m, --switch-mac TEXT           MAC Address of the switch who's port you
                                  wish to control  [required]
  -p, --switch-port INTEGER RANGE
                                  The port on the switch you wish to control
                                  [0<=x<=47;required]
  --help                          Show this message and exit.

Commands:
  cycle  Power cycle PoE port
  off    Turn off PoE port
  on     Turn on PoE port
```


# Thanks

- The [Ubiquiti Community wiki](https://ubntwiki.com) for their awesome work 
[documenting](https://ubntwiki.com/products/software/unifi-controller/api) the api.
- [Joe Stump](https://github.com/joestump) for their 
[api client implementation](https://gist.github.com/joestump/615ecf8ce744999ad536d7cc4750babb).
