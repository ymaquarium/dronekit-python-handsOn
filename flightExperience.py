from dronekit import connect, VehicleMode, Command
from pymavlink import mavutil
import time 

vehicle = connect("tcp:127.0.0.1:5762", wait_ready=True, timeout=60)
cmds = vehicle.commands

#Set Home Location
while not vehicle.home_location:
    cmds.download()
    cmds.wait_ready()

    if not vehicle.home_location:
        print("waiting for home location...")

print("Home Location: %s"%vehicle.home_location)

#arm
try:
    vehicle.wait_for_armable()
    vehicle.wait_for_mode("GUIDED")
    vehicle.arm()
except TimeoutError as takeoffError:
    print("Takeoff is timeout!!")

#mission clear
cmds.clear()

#Define mission
cmd1 = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0,0,0,0,0,0,0,0,10)
cmd2 = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0,0,0,0,0,0,5,0,10)
cmd3 = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0,0,0,0,0,0,0,5,10)
cmd4 = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0,0,0,0,0,0,0,0,10)
cmd5 = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0,0,0,0,0,0,0,0,0)

cmds.add(cmd1)
cmds.add(cmd2)
cmds.add(cmd3)
cmds.add(cmd4)
cmds.add(cmd5)
cmds.upload()

vehicle.mode = VehicleMode("AUTO")

#Notify mission complete
while True:
    print("commands.next :%s"%cmds.next)
    time.sleep(1)
