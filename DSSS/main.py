import adquisition

import numpy as np
import rtlsdr
from time import perf_counter
import pandas as pd


#Constants and Configuration:
DEBUG = True                          #Take GPS MAX2771 recorded file or RTL-SDR recording
AdquisitionTime = 10e-3               #[s]
SamplingRate = 4.0922e6               #[Hz]
TuneFrequency =1.57542e9              #[Hz]
Gain = 0                              #[dB]
DopplerRange = 20e3                   #[Hz]
DopplerBins = 300                     #Number of bins in the 'DopplerRange' (For optimal performance minimum of 100Hz resolution)

#Important note: Rigth now the system has not been proven to work with RTL-SDR
#                The reason for that is I dont have a good frontend for the GNSS (L1) band

#Update: I dont think I will use the RTL-SDR anymore, is preatty crappy for this. It can be used but better SDR are preatty cheap these days
#        Also this 'pyrtlsdr' does not support other common SDR, so upgradability is garbage. Conclusión the GNSS correlator works :), but hardware is really crappy

SampleLength = int(SamplingRate*AdquisitionTime / 1024) *1024
print(f'Sample Lenght = {SampleLength} [samples]')

if DEBUG:
    print('Reading file...')
    IQ_data = pd.read_csv('4.092_14_SM.csv')
    I_data = IQ_data['I']
    Q_data = IQ_data['Q']

    samples = I_data + 1j * Q_data
else:

    print('Taking Samples for RTL-SDR...')
    sdr = rtlsdr.RtlSdr(0)
    sdr.set_sample_rate(SamplingRate)
    sdr.set_manual_gain_enabled(1)
    sdr.set_gain(Gain)
    sdr.set_center_freq(TuneFrequency)
    sdr.set_bias_tee(enabled= True)

    samples = sdr.read_samples(SampleLength)
    sdr.close()

samples = samples - np.mean(samples) #Remove DC-Offset




adquiredSatellites = adquisition.adquire(inputSamples= samples, SamplingFrequency= SamplingRate, DopplerRange= DopplerRange, DopperlBinNumber= DopplerBins)

#Now will come the fun part: Tracking and Symbol Recovery, I've done it in embeded systems using 'Double Buffering' with a DMA (Direct Memory Acces) but in Python I guess I'll use MultiThreading at some point
