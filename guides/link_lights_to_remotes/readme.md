




# Linking lights and remotes directly (deCONZ)
This guide is heavily inspired by the works of [Claus Blaabjerg Hansen](https://rolig.dk/?p=1827&fbclid=IwAR2JTtbErRf8s97mQOSEeVbfch7PHsGondFJg0whd3_IE9d3FcfiYkLcnR0), but I think this version has a more simple and easy approach, since it does not use the deCONZ app.

By completing the numerous steps in this guide, you will end up having:
 1. a fail-safe solution, where lights still is operational although Home Assistant is down
 2. a prettier implementation of deCONZ groups in Home Assistant, because now the remote and the group is the same
## Introduction
The remote must be reset and free of any existing groups. Furthermore custom key bindings in Home Assistant will not function in a fail-safe situation.
### Tools needed
 1. a browser
 2. access to curl command, preferably in a SSH session or similar
### Steps
Here are the steps we need to perform:
 1. Open Phoscon for direct API calls
 2. Obtain a `token` from Phoscon
 3. Extract groups from Phoscon
 4. Find the ID (MAC address) of the remote(s)
 5. Edit the name of the group
 6. Add members (lights) to the group
 7. Enjoy a fail-safe solution
## Open Phoscon for direct API calls
In our daily use with Phoscon we do not need to forward ports, since we are using ingress in Home Assistant.
But to get the token and perform the needed task, we need to have a direct connection to Phoscon.
Therefore you will need to add port 40850 to your config af deCONZ. After the completion of this guide, the port is not longer needed.
![Configuration of the portforwarding in deCONZ](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/deconz_configuration.png)
## Getting token from Phoscon
I am merely using `curl` to obtain a token from Phoscon.
1. Open a SSH session to your Home Assistant, this can be from the:
		-	SSH add-on within Home Assistant
		-	a SSH session from your favourite SSH client
	In the name of simplicity I will be using a SSH session from within Home Assistant.
	![SSH session within Home Assistant](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/ha_ssh_session.png)
2.	 We need to prepare, but not fire, our request string in order to obtain the token from Phoscon.
	Replace the capitalized **YOUR_FICTIVE_APP_NAME** with a name of your liking and **YOUR_HA_IP** with the IP adsress of your Home Assistant.

    curl -X POST -d '{"devicetype":"YOUR_FICTIVE_APP_NAME"}' YOUR_DECONZ_IP:40850/api

3. Before we press `Enter`, we need to let Phoscon accept a new connection.
Therefore we need to open Phoscon and authourize our fictive app.
![Open the menu](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/phoscon_menu.png)
![Select gateway](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/phoscon_gateway.png)
![Enter advanced](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/phoscon_advanced.png)
![Click Authenticate app](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/phoscon_authenticate.png)
![Authentication is open](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/phoscon_open.png)
5. Let us hurry back to our SSH session and press enter.
	If everything worked as it should you will have result like this below:
![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/deconz_token.png)

I have redacted some of my token.

## Exctract groups from Phoscon
We need to find the ID of the remote, to do this we will need to extract all the groups in Phoscon.
 1.  Open a browser at enter the following URL, replacing the capitalized parts with your own info

    http://YOUR_DECONZ_IP:40850/api/YOUR_TOKEN/groups


 2. This will give you a output pretty much like this, maybe your browser is better to display JSON, but mine is not.
	![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/deconz_groups.png)
 3. To help us parse and find the wanted groups in the mess, lets go to [JSON Editor Online](https://jsoneditoronline.org/) and paste it all into the the left pane. Click "Copy >" and then "tree" in the right pane.
	![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/json_tree.png)
	**Keep this window open!!!**
## Finding the ID of the remote
In order the find the ID of the remote, we will need to find a its unique identifier (MAC address), to do this we can simpy listen for the deconz_event when one of the buttons on the remote is pressed. 

 4. We are using the developer tools of Home Assistant and a event listener `deconz_event` to find the ID of the remote. Press "START LISTENING" and here after a button on the remote.
 ![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/deconz_event.png)
 5. Copy this ID, which is actually the MAC address of the remote, and paste it into the search field of the JSON Editor.
 ![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/json_found_id.png)
 The ID of the remote is merely a key in the JSON data. It this case the ID is **95**.
 ## Edit the group
 1.  This is done in the **Wireless Light Control System**, not Phoscon or deCONZ.
	Alter this URL and paste it into a new browser window:

    http://YOUR_DECONZ_IP:40850/login.html
 2. Use these credentials to login
 	**User: delight
	Password: YOUR_PHOSCON_PASSWORD**
	![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/light_control_login.png)

 3. This will take your to a overview of entities in Phoscon/deCONZ.
	![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/light_control_start.png)
 4. Now we must find our remote - it quite easy....
	Click on the four dot on **any** group.
	![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/light_control_open.png)
 5. This will open the group, but not the group we want to edit. Therefore replace the ID in the URL with the ID of our group and press `enter`.
![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/light_control_id_before.png)
![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/light_control_id_after.png)
 6. Now we can rename the group/remote to our own liking:
![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/light_control_rename.png)
Press Done
![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/light_control_rename_done.png)
## Add lights to the group

 1. Now we must edit the group, click "Groups" in the top menu.
 ![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/light_control_groups.png)
 2. Now we can easily find the group and click "Edit members"
 ![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/light_control_group_members.png)   
 3. Where we can add or remove members (lights) of the group
 ![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/light_control_add.png)
 4. When done click "**Apply**" not "Done"
 ![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/light_control_apply.png)
## Finish
If we were using a round IKEA remote, it would now be visible in Phoscon
![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/phoscon_groups.png)
But since I have been using a square dimmer, it is not visible i Phoscon.
It is however visible in Home Assistant as a light, after we have done a update in the Services panel.
![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/ha_update.png)
![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/ha_the_remote.png)
![enter image description here](https://github.com/J-Lindvig/HomeAssistant/raw/master/guides/link_lights_to_remotes/images/ha_the_light.png)
