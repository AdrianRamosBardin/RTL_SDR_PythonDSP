#Library Imports
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from scipy import signal
import rtlsdr
import DSP
from scipy.io.wavfile import write

sdr = rtlsdr.RtlSdr()


#Device Configuration
sdr.sample_rate = 1.2e6      #[Hz]
sdr.center_freq = 106e6     #[Hz]
sdr.freq_correction = 60     #[PPM]
sdr.gain = 40            #Enable AGC

#Matplotlib Window
fig = plt.figure()
PSD_canvas = fig.add_subplot(2,1,2)
Audio_canvas = fig.add_subplot(2,2,2)
Filter_canvas = fig.add_subplot(2,2,1)



fileSignal = []

def animate(i): #Main animation & processing loop
    PSD_canvas.clear()
    Filter_canvas.clear()
    Audio_canvas.clear()

    samples = sdr.read_samples(100*1024)
    LPF_samples = DSP.LPF_FFT(samples, 400e3, 5, sdr.sample_rate)
    audio = DSP.WBFM_Demod(LPF_samples, 10)

    PSD_canvas.psd(samples, NFFT=1024, Fs=1.2, Fc=sdr.center_freq/1e6)
    Filter_canvas.psd(LPF_samples, NFFT=1024, Fs=1.2/5, Fc=0) 
    Audio_canvas.plot(audio)

    fileSignal.extend(audio)


try:
    anim = animation.FuncAnimation(fig, animate, interval = 20, cache_frame_data=False)
    plt.show()
    
except KeyboardInterrupt:
    pass
finally:
    sdr.close()

    f = r"C:/Users/Usuario/Desktop/Proyectos/RTL_SDR/WBFM/animation.mp4" 
    #writergif = animation.PillowWriter(fps = 30) 
    #anim.save(f, writer=writergif)

    scaled = np.int16(fileSignal/np.max(np.abs(fileSignal)) * 32767)
    write('outputAudio.wav', 24000, scaled)

                    
