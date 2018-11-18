# coding: utf-8
import numpy as np

def __lift(x,w):
    (c, s) = (w.real, w.imag)
    a = np.array([x.real, x.imag])
    if s == 0:
        pass
    elif c >= 0.0:
        a[0] += int(a[1]*(c-1)/s)
        a[1] += int(a[0]*s)
        a[0] += int(a[1]*(c-1)/s)
    else:
        a[0] += int(a[1]*(c+1)/s)
        a[1] += int(a[0]*(-s))
        a[0] += int(a[1]*(c+1)/s)
        a *= -1
    return complex(a[0], a[1])

def __ilift(x,w):
    (c, s) = (w.real, w.imag)
    a = np.array([x.real, x.imag])
    if s == 0:
        pass
    elif c >= 0.0:
        a[0] -= int(a[1]*(c-1)/s)
        a[1] -= int(a[0]*s)
        a[0] -= int(a[1]*(c-1)/s)
    else:
        a *= -1
        a[0] -= int(a[1]*(c+1)/s)
        a[1] -= int(a[0]*(-s))
        a[0] -= int(a[1]*(c+1)/s)
    return complex(a[0], a[1])

def fft(x):
    x = np.asarray(x)
    n = len(x)
    if n == 1:
        return x
    elif n==2:
        return np.array([x[0]+x[1], x[0]-x[1]])
    else:
        x = x.reshape((4,-1))
        w = np.exp(-2j*np.pi/n*np.arange(n//4))
        fftsx = fft( np.concatenate((x[0]+x[2],x[1]+x[3])))
        x0 = fftsx[0::2]
        x1 = fft( [__lift(a,b) for a, b in zip(x[0] - 1j*x[1] - x[2] + 1j*x[3], w)] )
        x2 = fftsx[1::2]
        x3 = fft( [__lift(a,b) for a, b in zip(x[0] + 1j*x[1] - x[2] - 1j*x[3], w**3)] )
        return np.column_stack((x0, x1, x2, x3)).flatten()

def ifft(x):
    x = np.asarray(x)
    n = len(x)
    if n == 1:
        return x
    elif n == 2:
        return np.array([(x[0]+x[1])/2, (x[0]-x[1])/2])
    else:
        w = np.exp(-2j*np.pi/n*np.arange(n//4))
        ifftsx = ifft(x[::2])
        x0 = ifftsx[:n//4]
        x1 = np.array([__ilift(a,b) for a,b in zip(ifft( x[1::4] ), w)])
        x2 = ifftsx[n//4:]
        x3 = np.array([__ilift(a,b) for a,b in zip(ifft( x[3::4] ), w*w*w)])
        return np.concatenate(((2*x0+x1+x3)/4, (1j*x1+2*x2-1j*x3)/4, (2*x0-x1-x3)/4, (-1j*x1+2*x2+1j*x3)/4))

def rfft(x):
    x = np.asarray(x)
    n = len(x)
    if n == 1:
        return x
    elif n==2:
        return np.array([x[0]+x[1], x[0]-x[1]])
    else:
        return fft(x)[:n//2+1]

def irfft(x):
    x = np.asarray(x)
    n = len(x)
    if n == 1:
        return x
    elif n==2:
        return np.array([(x[0]+x[1])/2, (x[0]-x[1])/2])
    else:
        return ifft(np.concatenate((x, x[-2:0:-1].conjugate())))
