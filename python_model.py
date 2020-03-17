import math
import pandas
import seaborn as sns
import matplotlib.pyplot as plt

sns.set()

def d_t_r(degree):
    return degree/180*math.pi

def r_t_d(rad):
    return rad*180/math.pi

def red(v):
    if v > 0:
        return 1
    elif v < 0:
        return -1
    else:
        return 0

def simulation(c):
    angles0 = []
    angles0_deg = []
    angles1 = []
    angles2 = []
    times = []
    periods = []

    x = []
    y = []

    measurement = False

    t = 0
    angle = c['initial_angle']
    v = 0
    a = 0
    for i in range(c['step_amount']):
        a = -c['gravity'] * math.sin(angle)
        drag = 1/2 * 0.47 * (2 * math.pow(c['diameter']/2, 2) * math.pi) * c['air_density'] * math.pow(v, 2)
        drag = min(drag, abs(a))

        v += (a - drag*red(drag)/c['mass']) * c['step_size']
        angle += v/c['length'] * c['step_size']

        angles0.append(angle)
        angles0_deg.append(r_t_d(angle))
        angles1.append(v)
        angles2.append(a)
        x.append(math.sin(angle)*c['length'])
        y.append(math.cos(angle)*c['length'])

        t += c['step_size']
        times.append(t)

        if not measurement:
            if abs(v) > 10*c['step_size']:
                measurement = True

        if measurement and abs(v) < 5*c['step_size'] and red(angle) == red(c['initial_angle']):
            measurement = False
            if len(periods) == 0:
                periods.append(t)
            else:
                periods.append(t - sum(periods))

    return pandas.DataFrame({'angle':angles0,
        'angle [°]': angles0_deg,
        'time [s]': times}), periods


conditions = {
    'diameter': 0.1,
    'density': 500,
    'mass': 0.2,
    'length': 1,
    'gravity': 9.81,
    'air_density': 1.2,
    'initial_angle':d_t_r(5),
    'step_amount':1000,
    'step_size':0.01
}


df, periods = simulation(conditions)

sns.relplot(x='time [s]', y='angle [°]', data=df, kind='line')
plt.show()
