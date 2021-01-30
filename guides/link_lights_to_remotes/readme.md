
# Linking lights and remotes directly (deCONZ)
This guide i heavily inspired by 
By completing the numerous steps in this guide, you will end up having:
 1. a fail-safe solution, where lights still is operational allthough Home Assistant is down
 2. a prettier implementation of deCONZ groups in Home Assistant
## Introduction
### tools needed
 3. a browser (duh)
 4. `curl` command
### Steps
Here are the steps we need to perform:
 1. Obtain a `token` from deCONZ (Phoscon)
## Getting token from deCONZ
I am merely using curl to obtain a token from deCONZ.
1. Open a SSH session to your Home Assistant, this can be from the:
		-	SSH add-on within Home Assistant
		-	a SSH session from your favourite SSH client
	In the name of simplicity I will be using a SSH session from within Home Assistant.
	![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/ha_ssh_session.png)
2.	 We need to prepare, but not fire, our request string to obtain the token.

    curl -X POST -d '{"devicetype":"YOUR_FICTIVE_APP_NAME"}' YOUR_HA_IP:40850/api
  
3. Before we press Enter, we need to let deCONZ accept a new connection.
![Open the menu](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/phoscon_menu.png)
![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/phoscon_gateway.png)
![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/phoscon_advanced.png)
![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/phoscon_authenticate.png)
![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/phoscon_open.png)
4. Let us hurry back to our SSH session and pres enter.
	If everything worked as it should you will have result like this below:
![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/deconz_token.png)
I have redacted some of my token.