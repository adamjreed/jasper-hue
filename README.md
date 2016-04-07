# jasper-hue
A plugin for Jasper that interfaces with Philips Hue lights.

Written by Adam Reed

# Steps to install

* Clone the repository
```
git clone https://github.com/adamjreed/jasper-hue.git
```
* Copy the module file
```
cp jasper-hue/Hue.py <path to jasper modules dir>
```
* Add the following to your profile.yaml file
```
hue:
  bridge_ip: '[local IP of your Hue bridge, ex. 192.168.0.10]'
  user: '[User key generated by the Hue bridge]'
```

# Trigger phrase
The plugin listens for the the following phrases
* Turn the [room name] lights [on|off]
* Set the [room name] lights to [quarter|half|three quarter|full] brightness