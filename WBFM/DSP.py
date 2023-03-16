import numpy as np
from numpy import fft
from scipy import signal

def LPF_FFT(samples: np.ndarray, Cutoff_Frequency: float, Decimation_Rate: int, sample_rate: int):
    bandLimit = int(Cutoff_Frequency*samples.size / sample_rate)

    F_Dom = fft.fft(samples)
    F_Dom [bandLimit+1 : -bandLimit]= 0


    filteredSignal = fft.ifft(F_Dom)
    filteredSignal = signal.decimate(filteredSignal, Decimation_Rate, ftype = 'iir')
    return filteredSignal


def WBFM_Demod(samples: np.ndarray, Decimation_Rate: int):
    #Get Phase Signal
    phaseSignal = np.unwrap(np.angle(samples))
    #Diffenciate the phase signal to get frequency
    outputSignal = np.convolve(phaseSignal, [1,-1], mode = 'valid')
    #Decimate signal
    outputSignal = signal.decimate(outputSignal, Decimation_Rate, ftype = 'iir')
    return outputSignal
    

