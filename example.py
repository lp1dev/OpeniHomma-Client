from client import probeDevices, setCustomColor, sendTCPPacket

address = probeDevices()
packet = setCustomColor(255, 100, 100)
sendTCPPacket(address, packet)
