import math
import matplotlib.pyplot as plt

engine = {
    "throttle" : 1,
    "max_combustion" : 10, # kg / s
    "out_vel" : 3000, # m / s
}

ball = {
    "pos" : [0, 0],
    "vel" : [0, 0],
    "acc" : [0, 0],
    "radius" : 1,
    "starting_mass" : 80,
    "fuel_mass" : 20,
    "angle" : 0,
    "dragCoefficient" : 0.45,
}

vel_start = 0
angle_start = 45
time_stamp = 0.001 # in seconds
air_density = 1.225

wind_speed = 10
wind_direction = -1

start_velX = math.cos(math.radians(angle_start)) * vel_start
start_velY = math.sin(math.radians(angle_start)) * vel_start

ball["angle"] = angle_start
ball["vel"] = [start_velX, start_velY]
ball["mass"] = ball["starting_mass"] + ball["fuel_mass"]

def calculateDrag (obj, vel):

    obj_cross_section = obj["radius"]**2 * math.pi
    drag_x = obj["dragCoefficient"] * vel[0] * vel[0] * obj_cross_section * air_density / 2
    drag_y = obj["dragCoefficient"] * vel[1] * vel[1] * obj_cross_section * air_density / 2
    return [drag_x, drag_y]

def updateEngine (obj, engine):
    d_fuel = engine["throttle"] * engine["max_combustion"] * time_stamp
    
    if d_fuel <= obj["fuel_mass"]:
        obj["fuel_mass"] -= d_fuel
    else:
        d_fuel = 0

    v_r = obj["vel"][1] + d_fuel * engine["out_vel"] / obj["mass"]

    return [0, v_r]

def update (obj):
    obj["acc"] = [0, -9.8]
    
    air_drag = calculateDrag(obj, obj["vel"])
    wind_drag = calculateDrag(obj, [wind_speed, 0])
    wind_drag[0] *= wind_direction
    engine_power = updateEngine (obj, engine)

    obj["mass"] = obj["starting_mass"] + obj["fuel_mass"]

    if obj["vel"][1] < 0:
        air_drag[1] *= -1

    obj["acc"][0] -= air_drag[0] / obj["mass"]
    obj["acc"][1] -= air_drag[1] / obj["mass"]

    obj["acc"][0] += engine_power[0] / obj["mass"]
    obj["acc"][1] += engine_power[1] / obj["mass"]
    
    obj["vel"][1] = engine_power[1]
    obj["vel"][0] += obj["acc"][0] * time_stamp
    obj["vel"][1] += obj["acc"][1] * time_stamp
 
    obj["pos"][0] += obj["vel"][0] * time_stamp
    obj["pos"][1] += obj["vel"][1] * time_stamp

data_x = [ball["pos"][0]]
data_y = [ball["pos"][1]]

data_vel_y = [ball["vel"][1]]
data_acc_y = [ball["acc"][1]]

time = [0]
i = 1

while ball["pos"][1] >= 0:
    update(ball)
    data_x.append(ball["pos"][0])
    data_y.append(ball["pos"][1])
    data_vel_y.append(ball["vel"][1])
    data_acc_y.append(ball["acc"][1])
    time.append(time_stamp * i)
    i += 1

figure, axis = plt.subplots(3, 1)
figure.suptitle("Flying rocket sim")

axis[0].plot(time, data_y)
axis[0].set_xlabel ("time [s]")
axis[0].set_ylabel ("y [m]")

axis[1].plot(time, data_vel_y)
axis[1].set_xlabel ("time [s]")
axis[1].set_ylabel ("vel y [m / s]")

axis[2].plot(time, data_acc_y)
axis[2].set_xlabel ("time [s]")
axis[2].set_ylabel ("acc y [m / s*s]")

print(f"Last Vy: {data_vel_y[-1]}")

plt.show()