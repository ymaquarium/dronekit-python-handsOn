from dronekit import connect, VehicleMode, Command
from pymavlink import mavutil
import time 

#connect
print("------Establishing Connection...------ ")
print("...")
vehicle = connect("tcp:127.0.0.1:5762", wait_ready=True, timeout=60)
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
except TimeoutError as takeoffError:
    print("Takeoff is timeout!!")

print("Changed to 'GUIDED'\n")

#mission clear
cmds.clear()

#Define mission
##cmd1 = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0,0,0,0,0,0,35.877272, 140.336378,10)
cmd2 = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0,0,0,0,0,0,35.877502, 140.336378,10)
cmd3 = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0,0,0,0,0,0,35.877272, 140.336638,10)
cmd4 = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0,0,0,0,0,0,35.877272, 140.336378,10)
cmd5 = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0,0,0,0,0,0,35.877272, 140.336378,0)

##cmds.add(cmd1)
cmds.add(cmd2)
cmds.add(cmd3)
cmds.add(cmd4)
cmds.add(cmd5)
cmds.upload()


print("---!!!Mission Start!!!---")
vehicle.simple_takeoff(10)
#vehicle.commands.next = 0
time.sleep(10)
vehicle.wait_for_mode("AUTO")

#Notify mission complete
cmdnext = 0
while True:
    if cmdnext - cmds.next == 3:
        break
    print("commands.next :%s"%cmds.next)
    cmdnext = cmds.next
    time.sleep(1)

print("\n---!!!MISSION FINISHED!!!---")
