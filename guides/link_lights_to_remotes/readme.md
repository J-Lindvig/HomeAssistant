



# Linking lights and remotes directly (deCONZ)
This guide i heavily inspired by 
By completing the numerous steps in this guide, you will end up having:
 1. a fail-safe solution, where lights still is operational allthough Home Assistant is down
 2. a prettier implementation of deCONZ groups in Home Assistant
## Introduction
The remote must be reset and free of any existing groups. Furthermore custom key bindings in Home Assistant will not perform in a fail-safe situation.
### tools needed
 1. a browser (duh)
 2. `curl` command
### Steps
Here are the steps we need to perform:
 1. Open deCONZ for direct API calls
 2. Obtain a `token` from deCONZ (Phoscon)
 3. Extract groups from deCONZ
 4. Find the ID (MAC address) of the remote(s)
 5. Edit the name of the group
 6. Add members (lights) to the group
 7. Enjoy a fail-safe solution
## Open deCONZ for direct API calls
In our daily use with deCONZ we do not need to forward ports, since we are using ingress in Home Assistant.
But to get the token and perform the needed task, we need to have a direct connection to deCONZ.
![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/deconz_configuration.png)
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

## Exctract groups from decONZ
 1.  Open a browser at enter the following URL, replacing the capitalized parts with your own info

    http://YOUR_HA_IP:40850/api/YOUR_TOKEN/groups


 2. This will give you a output pretty much like this, maybe your browser is better to display JSON, but mine is not.
	![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/deconz_groups.png)
 3. To help us parse and find the wanted groups in the mess, lets go to [JSON Editor Online](https://jsoneditoronline.org/) and paste it all into the the left pane. Be sure to click "tree" in the right pane.
	![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/json_tree.png)
	**Keep this window open!!!**
## Finding the ID of the remote

 4. We are using the developer tools of Home Assistant and a event listener `deconz_event` to find the ID of the remote.
 ![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/deconz_event.png)
 5. Copy this ID, which is actually the MAC address of the remote, and paste it into the search field of the JSON Editor.
 ![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/json_found_id.png)
 The ID of the remote is merely a key in the JSON data.
 ## Edit the group
 6.  This is done in the "light control", not Phoscon or deCONZ.
	Enter this url in a new browser window:

    http://YOUR_HA_IP:40850/login.html
 7. Use these credentials to login
	![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/light_control_login.png)
	**User: delight
	Password: YOUR_DECONZ_PASSWORD**
 8. This will take your to a overview of the current groups in deCONZ.
	![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/light_control_start.png)
 9. Now we must find our remote - it quite easy....
	Click on the four dot on any group.
	![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/light_control_open.png)
 10. This will open the group, but not the group we want to edit. Therefore replace the ID in the URL with the ID of our group.
![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/light_control_id_before.png)
![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/light_control_id_after.png)
 11. Now we can rename the group/remote to our own liking:
![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/light_control_rename.png)
Press Done
![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/light_control_rename_done.png)
## Add lights to the group

 1. Now we can find our remote in the "Group" view.
 ![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/light_control_groups.png)
 2. Now we can easily find the group
 ![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/light_control_group_members.png)   
 3. And edit the members (lights) of the group
 ![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/light_control_add.png)
 4. When done click "Apply" not "Done"
 ![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/light_control_apply.png)
## Finish
If we were using a round IKEA remote, it would now be visible in Phoscon
![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/phoscon_groups.png)
But since I have been using a square dimmer, it is not visible i Phoscon.
It is however visible in Home Assistant as a light, after we have done a update in the Services panel.
![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/ha_update.png)
![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/ha_the_remote.png)
![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/ha_the_light.png)