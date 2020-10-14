# %% fungsi-fungsi umum

def translate(value, leftMin, leftMax, rightMin, rightMax):
  leftSpan = leftMax - leftMin
  rightSpan = rightMax - rightMin
  valueScaled = float(value - leftMin) / float(leftSpan)
  return rightMin + (valueScaled * rightSpan)

def toDecimal(bin_list):
  dec = 0
  l = len(bin_list) - 1
  for i, x in enumerate(bin_list):
    dec += pow(2, l - i) * x
  return dec

# %% plotting

def histogram(arr:list):
  hist = {}
  for i in arr:
      hist[i] = hist.get(i, 0) + 1
  return hist