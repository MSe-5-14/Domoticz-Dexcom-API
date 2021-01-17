# Domoticz-Dexcom-API
This plugin allows you to retrieve real time glucose readings from the Dexcom Share API and insert them into Domoticz. 
This plugin uses the [pydexcom plugin](https://github.com/gagebenne/pydexcom) written by @gagebenne which does all the heavy lifting :smile: I just added the connection to domoticz.

## setup

* open a command prompt on your domoticz machine. 
* go to the domoticz installation folder.
* open the plugin folder.
* run  `git clone https://github.com/MSe-5-14/Domoticz-Dexcom-API.git Dexcom`
* open the domoticz web interface
* go to hardware and find the Dexcom Share API plugin

![DexcomDomoticz](https://user-images.githubusercontent.com/31540586/104842832-a1ba2800-58c7-11eb-9455-c27717a421ce.png)

* provide the information needed and click ADD
* under devices you should see two new devices
	* one with the current glucose measurement
	* one with the trend 

![DexcomDomoticz](https://user-images.githubusercontent.com/31540586/104842898-15f4cb80-58c8-11eb-8b93-ff5a57d8c13d.png)

* after adding them to your domoticz, you shoudl find two new entries under Uitility
![2021-01-17 13_31_46-Window](https://user-images.githubusercontent.com/31540586/104842937-6835ec80-58c8-11eb-88ed-eecc0caf7b79.png)
