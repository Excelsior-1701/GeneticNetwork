import GeneticPolynomial as GP


def pressure(moles, temp, volume):
    return moles * temp * 8.31 / volume


def bz_function(weights):
    plasma = weights[0]
    n2o = weights[1]
    temperature = weights[2]
    volume = weights[3]
    moles = plasma + n2o
    kpa = pressure(moles, temperature, volume)
    return min(1/((min(max(kpa, 1), 1000) / (0.5 * 101.75)) * (max(plasma / n2o, 1))),
               plasma / 2, n2o) / volume


plasma_range = {"min": 1, "max":1000}
n2o_range = {"min": 1, "max":1000}
temp_range = {"min": 23, "max": 1000}
volume_range = {"min": 1000, "max": 1000}
ranges = [plasma_range, n2o_range, temp_range, volume_range]
model = GP.Model(bz_function, ranges)
model.train(500)
vol_pressure_points = []
'''for vol in range(200, 20000, 200):
    volume_range["min"] = vol
    volume_range["max"] = vol + 100
    
    model.train(500)
    vol_pressure_points.append({vol: round(pressure(sum(model.best_fit[0:1]), model.best_fit[2], model.best_fit[3]), 2)})'''

print("Moles of Plasma/N2O, Temp K, Volume: ", model.best_fit)
print("Moles per volume: ", bz_function(model.best_fit))
print("Total Moles: ", bz_function(model.best_fit) * model.best_fit[3])
print("Operating Pressure: ", pressure(sum(model.best_fit[0:1]), model.best_fit[2], model.best_fit[3]))
