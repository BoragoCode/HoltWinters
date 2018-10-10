import pandas as pd
series = [3,10,12,13,12,10,12]
def average(series):
    return float(sum(series))/len(series)
print ("Promedio ",average(series))

def moving_average(series, n):
    return average(series[-n:])

print ("Promedio movil (3)",moving_average(series,3))
print ("Promedio movil (4)",moving_average(series,4))

def weighted_average(series, weights):
    result = 0.0
    weights.reverse()
    for n in range(len(weights)):
        result += series[-n-1] * weights[n]
    return result
weights = [0.1,0.2,0.3, 0.4]
print ("Promedio ponderado",weighted_average(series,weights))

def exponential_smoothing(series, alpha):
    result = [series[0]] # first value is same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n-1])
    return result
print ("Suavizamiento exponencial alpha bajo",exponential_smoothing(series, 0.1))
print ("Suavizamiento exponencial alpha alto",exponential_smoothing(series, 0.9))

series = [30,21,29,31,40,48,53,47,37,39,31,29,17,9,20,24,27,35,41,38,
          27,31,27,26,21,13,21,18,33,35,40,36,22,24,21,20,17,14,17,19,
          26,29,40,31,20,24,18,26,17,9,17,21,28,32,46,33,23,28,22,27,
          18,8,17,21,31,34,44,38,31,30,26,32]
df = pd.DataFrame(series)
plot=df.plot()
fig =plot.get_figure()
fig.savefig('salida.png')

def initial_trend(series, L):
    sum = 0.0
    for i in range(L):
        sum += float(series[i+L] - series[i]) / L
    return sum / L

def initial_seasonal_components(series, L):
    seasonals = {}
    season_averages = []
    n_seasons = int(len(series)/L)
    # compute season averages
    for j in range(n_seasons):
        season_averages.append(sum(series[L*j:L*j+L])/float(L))
    # compute initial values
    for i in range(L):
        sum_of_vals_over_avg = 0.0
        for j in range(n_seasons):
            sum_of_vals_over_avg += series[L*j+i]-season_averages[j]
        seasonals[i] = sum_of_vals_over_avg/n_seasons
    return seasonals

def triple_exponential_smoothing(series, slen, alpha, beta, gamma, n_preds):
    result = []
    seasonals = initial_seasonal_components(series, slen)
    for i in range(len(series)+n_preds):
        if i == 0: # initial values
            smooth = series[0]
            trend = initial_trend(series, slen)
            result.append(series[0])
            continue
        if i >= len(series): # we are forecasting
            m = i - len(series) + 1
            result.append((smooth + m*trend) + seasonals[i%slen])
        else:
            val = series[i]
            last_smooth, smooth = smooth, alpha*(val-seasonals[i%slen]) + (1-alpha)*(smooth+trend)
            trend = beta * (smooth-last_smooth) + (1-beta)*trend
            seasonals[i%slen] = gamma*(val-smooth) + (1-gamma)*seasonals[i%slen]
            result.append(smooth+trend+seasonals[i%slen])
    return result


print initial_trend(series,12)

print (initial_seasonal_components(series, 12))
