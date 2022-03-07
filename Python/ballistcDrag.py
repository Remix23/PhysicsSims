import math
import matplotlib.pyplot as plt

engine = {
    "throttle" : 1,
    "max_combustion" : 30, # kg / s
    "out_vel" : 0, # m / s
    "efficiency" : 0.8,
    "energy_per_kg" : 10000,
}

fuel_start_mass = 90

ball = {
    "pos" : [0, 0],
    "vel" : [0, 0],
    "acc" : [0, 0],
    "radius" : 1,
    "starting_mass" : 10,
    "fuel_mass" : fuel_start_mass,
    "angle" : 0,
    "drag_coefficient" : 0.45,
}

atmosphere_data = {
    "h": 0,
    "fg": 0,
    "temp" : 288,
    "pressure" : 101300,
    "density" : 0,
}

forces_to_work = {
    "airdrag_x" : 0,
    "airdrag_y" : 0,
    "engine_x" : 0,
    "engine_y" : 0,
    "gravity" : 0,
}

"""
wzór barometryczny 
p = p0 * exp(- miu * g * h / RT)
R - stała gazowa
miu - masa molowa powietrza 
T - temperatura 
p0 - 1013 hPa - 1013 * 10^2 Pa

gęstość 
ro = p / rt 

r - stała gazowa dla powietrza

temperatura

273K + 15 = 15 C

spada liniowo 
ziemia = 15C
100km = 0K
"""

p_ground = 101300
niu = 0.0289644 # masa molowa powietrza 
R = 8.3145 # uniwersalna stała gazowa 
r = 287.05 # stała gazowa dla powietrza 

earth_massG = 6.67243 * 5.9722 * (10**13)

vel_start = 0
angle_start = 45
time_stamp = 0.001 # in seconds

wind_speed = 0
wind_direction = -1

start_velX = math.cos(math.radians(angle_start)) * vel_start
start_velY = math.sin(math.radians(angle_start)) * vel_start

ball["angle"] = angle_start
ball["vel"] = [start_velX, start_velY]
ball["mass"] = ball["starting_mass"] + ball["fuel_mass"]

def calculateDrag (obj, vel, air_density):

    obj_cross_section = obj["radius"]**2 * math.pi
    drag_x = obj["drag_coefficient"] * vel[0] * vel[0] * obj_cross_section * air_density / 2
    drag_y = obj["drag_coefficient"] * vel[1] * vel[1] * obj_cross_section * air_density / 2
    return [drag_x, drag_y]

def updateEngine (obj, engine):
    engine["out_vel"] = math.sqrt(2 * engine["efficiency"] * engine["energy_per_kg"])
    d_fuel = engine["throttle"] * engine["max_combustion"] * time_stamp
    
    if d_fuel <= obj["fuel_mass"]:
        obj["fuel_mass"] -= d_fuel
        a = engine["out_vel"] * engine["max_combustion"] / obj["mass"]
    else:
        d_fuel = 0
        a = 0

    return [0, a]

def atmosphere (obj):
    fg = earth_massG / math.pow(obj["pos"][1] + 6371000, 2)
    temp = 288 * (1 - obj["pos"][1] / 100000)

    pressure = p_ground * math.exp(-niu*fg*obj["pos"][1] / (temp * R))
    density = pressure / (r * temp)
    atmosphere_data["h"] = obj["pos"][1]
    atmosphere_data["fg"] = fg
    atmosphere_data["temp"] = temp
    atmosphere_data["pressure"] = pressure
    atmosphere_data["density"] = density
    return fg, density

def update (obj):
    atm_data = atmosphere(obj)
    obj["acc"] = [0, -atm_data[0]]
    
    air_drag = calculateDrag(obj, obj["vel"], atm_data[1])
    wind_drag = calculateDrag(obj, [wind_speed, 0], atm_data[1])
    wind_drag[0] *= wind_direction
    engine_power = updateEngine (obj, engine)

    forces_to_work["airdrag_x"] = air_drag[0]
    forces_to_work["airdrag_y"] = air_drag[1]
    forces_to_work["gravity"] = -atm_data[0]
    forces_to_work["engine_x"] = atm_data[0]
    forces_to_work["engine_y"] = engine_power[1]

    # update rocket properties
    obj["mass"] = obj["starting_mass"] + obj["fuel_mass"]

    if obj["vel"][1] > 0:
        air_drag[1] *= -1
    
    if obj["vel"][0] > 0:
        air_drag[0] *= 1

    obj["acc"][0] += air_drag[0] / obj["mass"]
    obj["acc"][1] += air_drag[1] / obj["mass"]

    obj["acc"][0] += engine_power[0]
    obj["acc"][1] += engine_power[1] 
    
    obj["vel"][0] += obj["acc"][0] * time_stamp
    obj["vel"][1] += obj["acc"][1] * time_stamp
 
    obj["pos"][0] += obj["vel"][0] * time_stamp
    obj["pos"][1] += obj["vel"][1] * time_stamp

data_x = [ball["pos"][0]]
data_y = [ball["pos"][1]]

data_vel_y = [ball["vel"][1]]
data_acc_y = [ball["acc"][1]]

data = []

time = [0]
i = 1

while ball["pos"][1] >= 0:
    
    packet = {
        "x": ball["pos"][0],
        "y": ball["pos"][1],
        "vel_x": ball["vel"][0],
        "vel_y": ball["vel"][1],
        "acc_x": ball["acc"][0],
        "acc_y": ball["acc"][1],
        "time" : time_stamp * i,
    }
    for key, value in atmosphere_data.items():
        packet[key] = value
    for key, value in forces_to_work.items():
        if len(data) > 0:
            packet[f"w_{key}"] = value * (packet["y"] - data[-1]["y"])
        else:
            packet[f"w_{key}"] = 0
        
    #print(ball)
    data.append(packet)
    update(ball)
    i += 1

figure, axis = plt.subplots(3, 2)
figure.suptitle("Flying rocket sim")

axis[0, 0].plot([x["time"] for x in data], [x["y"] for x in data])
axis[0, 0].set_ylabel ("y [m]")

axis[1, 0].plot([x["time"] for x in data], [x["vel_y"] for x in data])
axis[1, 0].set_ylabel ("vel y [m / s]")

axis[2, 0].plot([x["time"] for x in data], [x["acc_y"] for x in data])
axis[2, 0].set_ylabel ("acc y [m / s*s]")

axis[0, 1].plot([x["time"] for x in data], [x["w_gravity"] for x in data])
axis[0, 1].set_ylabel ("W (Fg)")
axis[1, 1].plot([x["time"] for x in data], [x["w_airdrag_y"] for x in data])
axis[1, 1].set_ylabel ("W (Ft)")
axis[2, 1].plot([x["time"] for x in data], [x["w_engine_y"] for x in data])
axis[2, 1].set_ylabel ("W (Fe)")

for ax in axis.flat:
    ax.set_xlabel ('time [s]')

print(f"Last Vy: {data[-1]['vel_y']}")
print(sum([x["w_engine_y"] for x in data]))
print(fuel_start_mass * engine["energy_per_kg"]*engine["efficiency"]) #math.sqrt(engine["efficiency"])

plt.show()