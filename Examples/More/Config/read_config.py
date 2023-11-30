"""
Demonstrates how to read configuration settings on a LabJack.

Relevant Documentation:

LJM Library:
    LJM Library Installer:
        https://labjack.com/support/software/installers/ljm
    LJM Users Guide:
        https://labjack.com/support/software/api/ljm
    Opening and Closing:
        https://labjack.com/support/software/api/ljm/function-reference/opening-and-closing
    eReadNames:
        https://labjack.com/support/software/api/ljm/function-reference/ljmereadnames

T-Series and I/O:
    Modbus Map:
        https://labjack.com/support/software/api/modbus/modbus-map
    Hardware Overview(Device Information Registers):
        https://labjack.com/support/datasheets/t-series/hardware-overview

Note:
    Our Python interfaces throw exceptions when there are any issues with
    device communications that need addressed. Many of our examples will
    terminate immediately when an exception is thrown. The onus is on the API
    user to address the cause of any exceptions thrown, and add exception
    handling when appropriate. We create our own exception classes that are
    derived from the built-in Python Exception class and can be caught as such.
    For more information, see the implementation in our source code and the
    Python standard documentation.
"""
from labjack import ljm


# Open first found LabJack
handle = ljm.openS("ANY", "ANY", "ANY")  # Any device, Any connection, Any identifier
#handle = ljm.openS("T8", "ANY", "ANY")  # T8 device, Any connection, Any identifier
#handle = ljm.openS("T7", "ANY", "ANY")  # T7 device, Any connection, Any identifier
#handle = ljm.openS("T4", "ANY", "ANY")  # T4 device, Any connection, Any identifier
#handle = ljm.open(ljm.constants.dtANY, ljm.constants.ctANY, "ANY")  # Any device, Any connection, Any identifier

info = ljm.getHandleInfo(handle)
print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
      "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
      (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))

deviceType = info[0]

# Setup and call eReadNames to read configuration values from the LabJack.
if deviceType == ljm.constants.dtT4:
    # LabJack T4 configuration to read
    names = ["PRODUCT_ID", "HARDWARE_VERSION", "FIRMWARE_VERSION",
             "BOOTLOADER_VERSION", "SERIAL_NUMBER", "POWER_ETHERNET_DEFAULT",
             "POWER_AIN_DEFAULT", "POWER_LED_DEFAULT"]
else:
    # LabJack T7 and T8 configuration to read
    names = ["PRODUCT_ID", "HARDWARE_VERSION", "FIRMWARE_VERSION",
             "BOOTLOADER_VERSION", "WIFI_VERSION", "SERIAL_NUMBER",
             "POWER_ETHERNET_DEFAULT", "POWER_WIFI_DEFAULT",
             "POWER_AIN_DEFAULT", "POWER_LED_DEFAULT"]

numFrames = len(names)
results = ljm.eReadNames(handle, numFrames, names)

print("\nConfiguration settings:")
for i in range(numFrames):
    print("    %s : %f" % (names[i], results[i]))

# Close handle
ljm.close(handle)
