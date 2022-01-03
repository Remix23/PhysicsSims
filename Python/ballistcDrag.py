import math
import matplotlib.pyplot as plt

ball = {
    "pos" : [0, 0],
    "vel" : [0, 0],
    "acc" : [0, 0],
    "radius" : 1,
    "mas" : 1000,
    "angle" : 0,
    "dragCoefficient" : 0.45,
}

vel_start = 10
angle_start = 45
time_stamp = 0.001 # in seconds
air_density = 1.225

wind_speed = 10
wind_direction = -1

start_velX = math.cos(math.radians(angle_start)) * vel_start
start_velY = math.sin(math.radians(angle_start)) * vel_start

ball["angle"] = angle_start
ball["vel"] = [start_velX, start_velY]

def calculateDrag (obj, vel):

    obj_cross_section = obj["radius"]**2 * math.pi
    drag_x = obj["dragCoefficient"] * vel[0] * vel[0] * obj_cross_section * air_density / 2
    drag_y = obj["dragCoefficient"] * vel[1] * vel[1] * obj_cross_section * air_density / 2
    return [drag_x, drag_y]

def update (obj):
    obj["acc"] = [0, -9.8]

    air_drag = calculateDrag(obj, obj["vel"])
    wind_drag = calculateDrag(obj, [wind_speed, 0])
    wind_drag[0] *= wind_direction

    if obj["vel"][1] < 0:
        air_drag[1] *= -1

    obj["acc"][0] -= air_drag[0] / obj["mas"]
    obj["acc"][0] += wind_drag[0] / obj["mas"]
    obj["acc"][1] -= air_drag[1] / obj["mas"]
    
    obj["vel"][0] += obj["acc"][0] * time_stamp
    obj["vel"][1] += obj["acc"][1] * time_stamp

    obj["pos"][0] += obj["vel"][0] * time_stamp
    obj["pos"][1] += obj["vel"][1] * time_stamp



data_x = [ball["pos"][0]]
data_y = [ball["pos"][1]]

data_vel_y = [ball["vel"][1]]

time = [0]
i = 1

while ball["pos"][1] >= 0:
    update(ball)
    data_x.append(ball["pos"][0])
    data_y.append(ball["pos"][1])
    data_vel_y.append(ball["vel"][1])
    time.append(time_stamp * i)
    i += 1

figure, axis = plt.subplots(2, 1)

axis[0].plot(data_x, data_y)
axis[1].plot(time, data_vel_y)

print(f"Last Vy: {data_vel_y[-1]}")

plt.show()