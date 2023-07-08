from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import math

def reached_target_location(target_location):
    """
    目標の位置に到達したかどうかを判定する関数
    """
    current_location = vehicle.location.global_relative_frame
    distance = get_distance_metres(current_location, target_location)
    return distance < 1.5  # 目標に1.5m以内であれば到達したとみなす


def get_distance_metres(location1, location2):
    """
    2つの位置情報間の距離をメートル単位で計算する関数
    """
    dlat = location2.lat - location1.lat
    dlong = location2.lon - location1.lon
    dalt = location2.alt - location1.alt 
    distance_2d = math.sqrt((dlat*dlat) + (dlong*dlong))  # 直線距離を計算する
    distance_3d = math.sqrt((distance_2d*distance_2d) + (dalt*dalt))  # 3次元距離を計算する
    return distance_3d * 1.113195e5


def vertical_move(point, target_location):
    """
    ある地点へ移動し、ホバリング、5mずつ15m高度を下げ、最初の地点へ戻る
    """

    # 地点へ移動し、ホバリング
    print("Going to "+point)
    vehicle.simple_goto(target_location)

    while not reached_target_location(target_location):
        time.sleep(1)

    print("Hovering at "+point)

    time.sleep(5)  # 5秒間ホバリング

    # 降下とホバリング
    target_location.alt -= 5  # 5m降下
    vehicle.simple_goto(target_location)

    while not reached_target_location(target_location):
        time.sleep(1)

    print("Hovering at 5m below "+point)
    time.sleep(5)  # 5秒間ホバリング

    target_location.alt -= 5  # さらに5m降下
    vehicle.simple_goto(target_location)

    while not reached_target_location(target_location):
        time.sleep(1)

    print("Hovering at 10m below "+point)
    time.sleep(5)  # 5秒間ホバリング

    target_location.alt -= 5  # さらに5m降下
    vehicle.simple_goto(target_location)

    while not reached_target_location(target_location):
        time.sleep(1)

    print("Hovering at 15m below "+point)
    time.sleep(5)  # 5秒間ホバリング

    # 地点Bへ移動し、ホバリング
    target_location.alt +=15  # 地点Bへ戻る
    vehicle.simple_goto(target_location)

    while not reached_target_location(target_location):
        time.sleep(1)

    print("Hovering at point "+point+" again")
    time.sleep(5)  # 5秒間ホバリング


# ドローンへの接続
vehicle = connect('tcp:127.0.0.1:5762',wait_ready=False,timeout=60)
print("Connected.")

# 離陸
try:
    vehicle.wait_for_armable() #モード変更＋変更されるまで待つ
    vehicle.wait_for_mode("GUIDED")
    print("GUIDED")

    vehicle.arm()
    print("armed")
    time.sleep(1)

    vehicle.wait_simple_takeoff(30, timeout=20)
    print("takeoff")

except TimeoutError as takeoffError:
    print("Takeoff is timeout!!!")

time.sleep(5)

# 地点Aの座標を指定
latitude_A = 35.878812750  # 地点Aの緯度を指定
longitude_A = 140.3390620  # 地点Aの経度を指定
altitude_A = 30            # 地点Aの高度を指定

# 地点Aへ移動し、ホバリング
target_location_A = LocationGlobalRelative(latitude_A,longitude_A,altitude_A) # 地点Aの位置情報を設定する

print("Going to point A")
vehicle.simple_goto(target_location_A)

while not reached_target_location(target_location_A):
    time.sleep(1)

print("Hovering at point A")
time.sleep(10)  # 10秒間ホバリング

# 地点Bの座標を算出
latitude_B = latitude_A + 0.00009  # 地点Aから北に約10m
longitude_B = longitude_A  # 地点Aと経度は同じ
altitude_B = altitude_A

# 地点Bの位置情報を設定する
target_location_B = LocationGlobalRelative(latitude_B, longitude_B, altitude_B)  

# 地点Bへ移動し、ホバリング、垂直移動
vertical_move("point B", target_location_B)

# 地点Cの座標を算出
latitude_C = latitude_A  # 地点Aと緯度は同じ
longitude_C = longitude_A + 0.00009  # 地点Aから東に約10m
altitude_C = altitude_A

# 地点Cの位置情報を設定する
target_location_C = LocationGlobalRelative(latitude_C, longitude_C, altitude_C)  

# 地点Cへ移動し、ホバリング、垂直移動
vertical_move("point C", target_location_C)

# 離陸地点へ戻り、着陸
print("Returning to launch")
vehicle.mode = VehicleMode("RTL")

while vehicle.mode.name != "RTL":
    time.sleep(1)

while vehicle.armed:
    time.sleep(1)

print("Landed")

# ドローンとの接続解除
vehicle.close()
