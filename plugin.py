# Dexcom Python Plugin 
#
# Author: Maurice Seen
#
"""
<plugin key="Dexcom" name="Dexcom Share API" author="Maurice Seen" version="0.1.0">
    <description>
        <h2>Dexcom Share API</h2>
        <p>This plugin connects to dexcom share api and get the real time blood glucose information. This plugin is based on the & <a href="https://github.com/gagebenne/pydexcom" target="_blank"> PyDexcom project</a>.</p>
        <h3>Be aware</h3>
        <ul>
            <li>The service requires setup of at least one follower to enable the share service.</li>
            <li> The credentials requested below are of the sharer not the follower.</li>
            <li>Usernames and password with non alphanumeric characters may not work.</li>
        </ul>
        <h3>Settings</h3>
        <p></p>
    </description>
    <params>
        <param field="Username" label="Username" width="300px" required="true" />
        <param field="Password" label="Password" width="300px" required="true" password="true"/>
        <param field="Mode1" label="Outside of USA" width="150px">
            <options>
                <option label="True" value="True" default="true"/>
                <option label="False" value="False" />
            </options>
        </param>
        <param field="Mode2" label="Unit of measurement" width="150px">
            <options>
                <option label="mg/dl" value="mg_dl" default="true"/>
                <option label="mmol/l" value="mmol_l" />
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
from pydexcom import Dexcom

class BasePlugin:
    enabled = False
    
    def __init__(self):
        
        return

    def onStart(self):
        Domoticz.Log("onStart called")
        # setting Heartbeat to 20 seconds.
        Domoticz.Heartbeat(20)
        
        # check if icons are installed
        if ("Dexcom" not in Images):
           Domoticz.Image('Dexcom.zip').Create()
        
        if (len(Devices) == 0):
            
            Domoticz.Log("Creating devices in domoticz")

            # Create first device  
            if (Parameters["Mode2"] == "mg_dl"):
                Domoticz.Log("Measurement unit mg/dL")
                Domoticz.Device(Name="Glucose Level", Unit=1, TypeName="Custom", Options={"Custom": "1;mg/dL"}, Image=Images['Dexcom'].ID).Create()
            elif (Parameters["Mode2"] == "mmol_l"):
                Domoticz.Log("Measurement unit mmol/L")
                Domoticz.Device(Name="Glucose Level", Unit=1, TypeName="Custom", Options={"Custom": "1;mmol/L"}, Image=Images['Dexcom'].ID).Create()
            
            Domoticz.Device(Name="Glucose Trend", Unit=2, Type=243, Subtype=19, Image=Images['Dexcom'].ID).Create()
        

        
        # get current values
        self.GetCurrentValues()
        
    def GetCurrentValues(self):
        if (Parameters["Mode1"] == "True"):
            dexcom = Dexcom(Parameters["Username"], Parameters["Password"],"OUS=True")
        else:
            dexcom = Dexcom(Parameters["Username"], Parameters["Password"])

        bg = dexcom.get_current_glucose_reading()

        if hasattr(bg, 'value'):
        
            if (Parameters["Mode2"] == "mg_dl"):
                Measurement = bg.value
            else:
                Measurement = bg.mmol_l
            
            if type(Measurement) == int:
                UpdateDevice(1, Measurement, str(Measurement), 0)
                UpdateDevice(2, bg.trend, str(bg.trend_description), 0)
        else:
            UpdateDevice(2, 0, "No Data", 0)
    
    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        
        self.GetCurrentValues()

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return

def UpdateDevice(Unit, nValue, sValue, TimedOut):
    # Make sure that the Domoticz device still exists (they can be deleted) before updating it 
    if (Unit in Devices):
        if (Devices[Unit].nValue != nValue) or (Devices[Unit].sValue != sValue) or (Devices[Unit].TimedOut != TimedOut):
            Devices[Unit].Update(nValue=nValue, sValue=str(sValue), TimedOut=TimedOut)
            Domoticz.Log("Update "+str(nValue)+":'"+str(sValue)+"' ("+Devices[Unit].Name+")")
    return
