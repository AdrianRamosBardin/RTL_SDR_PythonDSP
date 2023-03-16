This simple code demodulates a near Wide Band Frequency Modulated station (WBFM). The main objective was to build the plot in Matplotlib to see in realtime the signal processing.
With that said when I finished writing the script I wanted to hear the Audio so I used Scipy for making it possible, but the performance its really crappy. In the near future I may change the whole structure of the demodulator by getting rid of the GUI and implementing a callback system.
Implementing the processing in the callback function will allow for real time audio stream, I really enjoy listening to 'Cadena SER' but I may use this to make a crude real time analog video link for a long range rocket.

In the added screenshot of the animated GUI we can see 3 plots, the bootom one is the PSD(Power Spectral Density) of the SDR signal, the top-left is the same but digitally filtered to see only the radio station we are interested on. And finally the top-right is the demodulated audio signal

A.Ramos
