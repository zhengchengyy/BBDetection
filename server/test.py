import numpy as np
import matplotlib.pyplot as plt
import pywt

t = np.linspace(0, 1, 400, endpoint=False)
cond = [t<0.25, (t>=0.25)&(t<0.5), t>=0.5]
f1 = lambda t: np.cos(2*np.pi*10*t)
f2 = lambda t: np.cos(2*np.pi*50*t)
f3 = lambda t: np.cos(2*np.pi*100*t)

y1 = np.piecewise(t, cond, [f1, f2, f3])
y2 = np.piecewise(t, cond, [f2, f1, f3])

cwtmatr1, freqs1 = pywt.cwt(y1, np.arange(1, 200), 'cgau8', 1/400)
cwtmatr2, freqs2 = pywt.cwt(y2, np.arange(1, 200), 'cgau8', 1/400)

plt.figure(figsize=(12, 9))
plt.subplot(221)
plt.plot(t, y1)
plt.title('signal_1 in time domain')
plt.xlabel('Time/second')

plt.subplot(222)
plt.contourf(t, freqs1, abs(cwtmatr1))
plt.title('time-frequency relationship of signal_1')
plt.xlabel('Time/second')
plt.ylabel('Frequency/Hz')

plt.subplot(223)
plt.plot(t, y2)
plt.title('signal_2 in time domain')
plt.xlabel('Time/second')

plt.subplot(224)
plt.contourf(t, freqs2, abs(cwtmatr2))
plt.title('time-frequency relationship of signal_2')
plt.xlabel('Time/second')
plt.ylabel('Frequency/Hz')

plt.tight_layout()
plt.show()