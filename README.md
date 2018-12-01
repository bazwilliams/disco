# Build

Rename the hue_lights as appropriate for your house. 

```sh
docker build -t disco .
```

# Run

Press the button on your Hue bridge

```sh
docker run disco
```

# Dance

```sh
mosquitto_pub -t house/livingroom/disco -m "On"
```

```
spotify:user:barryjohnwilliams:playlist:1Ut5juChbYvoqSeUK56Fct
```

```sh
mosquitto_pub -t house/livingroom/disco -m "Off"
```

# Improve

- [X] Use MQTT to turn disco mode on or off
- [ ] Configurable hue_lights
- [ ] Configurable bridge or auto discovery
- [ ] Use Spotify Web API to start music; or
- [ ] Hook into HomeAssistant