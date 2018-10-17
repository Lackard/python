import pint

ureg = pint.UnitRegistry()

flow1 = 10 * ureg.meter**3 / ureg.second
concen1 = 0.5
flow2 = 2 * ureg.meter**3 / ureg.second
concen2 = 0.5
flow3 = 7 * ureg.meter**3 / ureg.second

current_volume = 0.0 * ureg.meter**3
last_volume = 0.0 * ureg.meter**3

average_concen = 0.0
last_average_concen = 0.0

current_substance_volume = 0.0
delta_current_substance_volume = 0.0
last_substance_volume = 0.0

concen_requested_value = 0.5

error = 0.0
last_error = 0.0

def Step():
    global flow1
    global flow2
    global flow3
    global current_volume
    global last_volume
    global average_concen
    global last_average_concen
    global concen1
    global concen2
    global current_substance_volume
    global delta_current_substance_volume
    global last_substance_volume

    current_volume = (flow1 + flow2 - flow3) * ureg.second + last_volume
    last_volume = current_volume

    average_concen = ((concen1 - last_average_concen)*(flow1*ureg.second) + (concen2 - last_average_concen)*(flow2*ureg.second))/((flow1+flow2)*ureg.second) + last_average_concen
    last_average_concen = average_concen
    last_substance_volume = current_substance_volume


    print("Aktualna ilość substancji: {}".format(average_concen*current_volume))
    print("Aktualna ilość mieszaniny: {}".format(current_volume))
    print("Aktualne stężęnie substancji {}:".format(average_concen))


def regulator():
    global average_concen
    global concen_requested_value
    global concen1
    global error
    global last_error
    global flow1

    error = concen_requested_value - average_concen
    u = 0.001*(1 + (error + last_error)*840) #* ureg.meter**3/ureg.second
    print("U: {}".format(u.__round__()))
    last_error = error
    if u <0:
        concen1 += u
    if concen1 > 1:
        concen1 = 1
    else:
        concen1+=u
    print("Concen1: {}".format(concen1.__round__(3)))

for i in range(300):
    print("Stan w chwili {}:".format(i + 1))
    regulator()
    Step()

