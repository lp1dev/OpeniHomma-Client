# Open iHomma Client

	Free (GPLv3) Python client for iHomma smart devices
	developed and tested with the iHomma LED Smart Spot.
	This client should work with other smart devices compatible
	with the iHomma HCS Application.

# Installation

This client has been written for Python3.7,
it shouldn't require any additional module installation

# Usage

The client is more of a dev-oriented API at the moment.

A set of functions are available and allow to send instructions to your smart light's TCP server and
discover devices on your network.

# Example

```python
from client import probeDevices, setCustomColor, sendTCPPacket

address = probeDevices() #Returns a tuple containing the found device's IP and port 8080
packet = setCustomColor(255, 100, 100) #setCustomColor builds and returns a packet
sendTCPPacket(address, packet)

```

# Documentation

## probeDevices()

   Probes the network for live smart lights and returns the first device's address

## getLampJSONData()

   Returns the smart light's configuration as a JSON-formatted string

## setPredefinedLight(id)

   Sets the light's predefined color referenced by id.
   The ids from 0 to 9 are "static" colors.
   The ids from 10 to 19 are "animated" colors.

- 0: Strong white/yellow (strong, warm)                                                                                                
- 1: Candlelight                                                                                                                       
- 2: Morning Light (strong, warm)                                                                                                      
- 3: Nature Light (strong, white)                                                                                                      
- 4: Snow Light (strong, cold)                                                                                                         
- 5: Squirrel Light (soft, red)                                                                                                        
- 6: Coffee Light (soft, chill)                                                                                                        
- 7: Desk Light (strong, good for working)                                                                                             
- 8: Hipster food light. (strong, very white)                                                                                          
- 9: Yellow light (soft, warm)

- 10: 0xa  => Buggy? red (soft, pure red)                                                                                              
- 11: 0xb  => Slow rotation of all white luminescent colors                                                                            
- 12: 0xc  => Slow rotation from yellow (Morning)                                                                                      
- 13: 0xd  => Circle (cycles on all colors smoothly)                                                                                   
- 14: 0xe  => Party (cycles on all colors less smoothly)                                                                               
- 15: 0xf  => Romantic colors (Smooth from purple to red)                                                                              
- 16: 0x10 => Smooth yellow/red                                                                                                        
- 17: 0x11 => Blue wave                                                                                                                
- 18: 0x12 => Strong green gradient                                                                                                    
- 19: 0x13 => Strong white/yellow alternate

## setWarmth(value)

   Sets the light's color "warmth" (value is between 0 and 200)

## setLuminance(value)

   Set the light's luminance (value is between 0 and 200)

## setCustomColor(red, green, blue)

   Assign a custom RGB color to the light (values are between 100 and 255)

## setAbsoluteColor(color)

   Set the lamp to an "absolute" color (255, 0, 0) or (0, 255, 0) or (0, 0, 255).
   The color is referenced by the color parameter which can be "red", "green" or "blue"

## turnOnOff(value)

   Turns the lamp on and off, if value is True the lamp is turned on, and off if value is False.

## Licence

This project is using a GPLv3 licence that you can read in the LICENCE file.