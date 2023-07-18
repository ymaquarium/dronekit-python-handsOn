from dronekit import connect, VehicleMode, Command
from pymavlink import mavutil
import time 

#connect
print("------Establishing Connection...------ ")
print("...")
vehicle = connect("127.0.0.1:14552", wait_ready=True, timeout=60)
cmds = vehicle.commands
print("\n------Connected!------\n")
time.sleep(2)

#Set Home Location
while not vehicle.home_location:
    cmds.download()
    cmds.wait_ready()

    if not vehicle.home_location:
        print("waiting for home location...")

print("Home Location: %s"%vehicle.home_location)
time.sleep(2)

#arm
print("\nChanging mode to 'GUIDED'...")
try:
    vehicle.wait_for_armable()
    vehicle.wait_for_mode("GUIDED")
    vehicle.armed = True
    while not vehicle.armed:
        time.sleep(1)
except TimeoutError as takeoffError:
    print("Takeoff is timeout!!")

print("Changed to 'GUIDED'\n")

#option change tempolary
current_option = vehicle.parameters['AUTO_OPTIONS']
vehicle.parameters['AUTO_OPTIONS'] = 3

#mission clear
cmds.clear()

#Define mission
cmd1 = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0,0,0,0,0,0,0,0,10)
cmd2 = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0,0,0,0,0,0,35.878812598463035, 140.3394132748464,10)
cmd3 = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0,0,0,0,0,0,35.87862092608203, 140.33938888754727,10)
cmd4 = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0,0,0,0,0,0,35.878583381953064, 140.33916208566507,10)
cmd5 = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0,0,0,0,0,0,35.878583381953064, 140.33916208566507,0)

cmds.add(cmd1)
cmds.add(cmd2)
cmds.add(cmd3)
cmds.add(cmd4)
cmds.add(cmd5)
cmds.upload()


print("---!!!Mission Start!!!---")
vehicle.commands.next = 0
vehicle.wait_for_mode("AUTO")

#Notify mission complete
cmdnext = 0
while cmdnext - cmds.next != 4:
    if cmdnext != cmds.next:
        print("commands.next :%s"%cmds.next)
    cmdnext = cmds.next
    time.sleep(1)

# option change
vehicle.parameters["AUTO_OPTIONS"] = current_option

print("\n---!!!MISSION FINISHED!!!---")
