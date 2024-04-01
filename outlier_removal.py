import matplotlib.pyplot as plt

### --- parameters
max_index = []
max_eV = []
quad_ini = 0
quad_las = 0
fit_ylim_ini = 0
fit_ylim_las = 0

### --- denoise
acc_thres = 0.03**2 # parameter
cropped_index = max_index[quad_ini:quad_las]
cropped_eV = max_eV[quad_ini:quad_las]


def linear_interpolation(prevPoint, rate_of_change):
    return prevPoint + rate_of_change


# populated interpolated_eV 
interpolated_eV = [cropped_eV[0], cropped_eV[1]]
prev_vals = [cropped_eV[0], cropped_eV[1]] # initial value
for ind, val in enumerate(cropped_eV[2:]):
    rate = val - prev_vals[1]
    prev_rate = prev_vals[1] - prev_vals[0]
    acceleration = rate - prev_rate

    if (acceleration**2 > acc_thres):
        res = linear_interpolation(prev_vals[1], prev_rate)
        interpolated_eV.append(res)
        # print(ind + 1, "acceleration", acceleration, "prev_vals", prev_vals, "interpolation res", res)
        prev_vals[0] = prev_vals[1]
        prev_vals[1] = res
    else:
        interpolated_eV.append(val)
        prev_vals[0] = prev_vals[1]
        prev_vals[1] = val

    # print(acceleration, prev_vals)


# display result
print(interpolated_eV)
plt.plot(cropped_index, interpolated_eV)
plt.ylim(fit_ylim_ini,fit_ylim_las)
plt.xlabel('Pixel')
plt.ylabel('Energy (eV)')