import socket
from sys import argv
from time import sleep

# Globals

UDP_IP = "255.255.255.255"
UDP_PORT = 988
TCP_IP = argv[1] if len(argv) > 1 else ""
TCP_PORT = 8080
DEBUG_NETWORK = False
PACKET_SIZES = [752, 1008, 1009, 1010, 1266, 1522, 5677]

# Network Functions

def parseMessage(message):
    if type(message) == bytes:
        return message
    else:
        return message.encode()

def sendUDPPacket(address, message, wait_response=True):
    packet = parseMessage(message)
    if DEBUG_NETWORK:
        print("UDP target IP:", UDP_IP)
        print("UDP target port:", UDP_PORT)
        print("message string:", packet)
        print("message bytes:", packet)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sent = sock.sendto(packet, (UDP_IP, UDP_PORT))
    if wait_response:
        try:
            sock.settimeout(1)
            return sock.recvfrom(2048)
        except Exception as e:
            print(e)
            return None
    return sent

def sendTCPPacket(address, message, wait_response=False):
    packet = parseMessage(message)
    if DEBUG_NETWORK:
        print("TCP target IP:", address[0])
        print("TCP target port", address[1])
        try:
            print("message string:", packet.decode())
        except Exception as e:
            pass
        print("message bytes", packet)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    sent = sock.send(packet)
    if wait_response:
        try:
            sock.settimeout(0.3)
            response = sock.recv(1024)
            return [hex(byte) for byte in response]
        except Exception as e:
            print(e)
    return sent

# Lamp Functions

def probeDevices():
    deviceId, address = sendUDPPacket((UDP_IP, UDP_PORT), "HLK")
    print("Device discovered : %s" %deviceId, address[0])
    return (address[0], 8080)

def sendInstruction(instruction, write_switch, data, final_byte=0):
    header = [0xfe, 0xef]
    message_length = len(data) + 1 + 1 + 1 + (1 if final_byte else 0)# data + instruction + write_switch + last_byte
    packet = header + [message_length, instruction, write_switch] + data
    packet_size = final_byte
    last_byte = 0
    for byte in packet:
        packet_size += byte
    for size in PACKET_SIZES:
        if size >= packet_size:
            last_byte = size - packet_size + (1 if final_byte else 0)
            print('Last byte:', last_byte, "size", size)
            if last_byte > 255:
                continue
            packet.append(last_byte)
            if final_byte:
                packet.append(final_byte)
            print('last_byte', last_byte, packet_size + last_byte)
            print('Packet bytes', packet)
            return bytes(packet)
    packet[2] -= 1
    packet.append(final_byte)
    print(packet)
    return bytes(packet)

def getLampJSONData():
    return sendInstruction(0x2e, 0, [0xff])

def setPredefinedLight(lightId): # IDs are between 0 and 19
    """
    0: Strong white/yellow (strong, warm)
    1: Candlelight
    2: Morning Light (strong, warm)
    3: Nature Light (strong, white)
    4: Snow Light (strong, cold)
    5: Squirrel Light (soft, red)
    6: Coffee Light (soft, chill)
    7: Desk Light (strong, good for working)
    8: Hipster food light. (strong, very white)
    9: Yellow light (soft, warm)

    # 10 - 19 : Animations

    10: 0xa  => Buggy? red (soft, pure red)
    11: 0xb  => Slow rotation of all white luminescent colors
    12: 0xc  => Slow rotation from yellow (Morning)
    13: 0xd  => Circle (cycles on all colors smoothly)
    14: 0xe  => Party (cycles on all colors less smoothly)
    15: 0xf  => Romantic colors (Smooth from purple to red)
    16: 0x10 => Smooth yellow/red
    17: 0x11 => Blue wave
    18: 0x12 => Strong green gradient
    19: 0x13 => Strong white/yellow alternate
    """
    print("setPredefinedLight : %s" %lightId)
    return sendInstruction(0xa5, 1, [lightId])
 
def setWarmth(value): #value between 0 and 200
    print("setWarmth : %s" %value)
    return sendInstruction(0xa1, 1, [value], 94)

def setLuminance(value): #value between 0 and 200
    print("setLuminance : %s" %value)
    return sendInstruction(0xa7, 1, [value])

def setCustomColor(r, g, b): # value between 0 and 255
    print("setCustomColor : rgb(%s, %s, %s)" %(r, g, b))
    return sendInstruction(0xa1, 1, [r,g,b])

def setAbsoluteColor(color): 
    if color == "red":
        return sendInstruction(0xa1, 1, [255, 0, 0], 94)
    elif color == "green":
        return sendInstruction(0xa1, 1, [0, 255, 0], 94)
    elif color == "blue":
        return sendInstruction(0xa1, 1, [0, 0, 255], 94)

def turnOnOff(on):
    print("turnOnOff : %s" %on)
    value = 17 if on else 18
    return sendInstruction(0xa3, 1, [value])
