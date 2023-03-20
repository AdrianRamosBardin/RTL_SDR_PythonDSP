import GoldCode_Generator
import numpy as np



def adquire(inputSamples, SamplingFrequency, DopplerRange, DopperlBinNumber):
    #Esta función devulve un array con los satélites adquiridos

    NumberOfSamples = len(inputSamples)
    print('Number of Samples: ' + str(NumberOfSamples))

    SampleLength_time = NumberOfSamples/SamplingFrequency
    timeVector = np.linspace(0, SampleLength_time, NumberOfSamples)
    print('Sample Length (time): ' + str(max(timeVector)))

    Satellites = []
    for i in range(1,33):
        sat = GNSS_Satellite(i)
        Satellites.append(sat)

    maxDopperlFrequency = DopplerRange/2
    minDopperlFrequency = -DopplerRange/2
    DopplerBins = np.linspace(minDopperlFrequency, maxDopperlFrequency, DopperlBinNumber)

    for satellite in Satellites:

        print('Searching for Satellite: ' + str(satellite.get_PRN_Num()) + ':')
        for DopplerShift in DopplerBins:
            #print(' -> Doppler Frequency: ' + str(DopplerShift))
            GoldCode = satellite.get_PRN_Code()

            
            GoldCode_Sampled = []
            for num in GoldCode:
                PRN_Rate = 1.023e6
                for j in range(int(SamplingFrequency/PRN_Rate)):
                    GoldCode_Sampled.append(num)

            GoldCode_Resampled = np.tile(GoldCode_Sampled, int(NumberOfSamples/len(GoldCode_Sampled)))

            GoldCode_Fft = np.fft.fft(GoldCode_Resampled, NumberOfSamples)
            GoldCodeFft_conj = np.conjugate(GoldCode_Fft)

            shiftedSamples = inputSamples*np.exp(-1j*2*np.pi*DopplerShift*timeVector)
            shiftedFft = np.fft.fft(shiftedSamples, NumberOfSamples)

            result = np.fft.ifft(GoldCodeFft_conj * shiftedFft, NumberOfSamples)
            resultSQ = np.real(result * np.conjugate(result))

            rmsPowerdB = 10*np.log10(np.mean(resultSQ))
            resultdB = 10*np.log10(resultSQ)

            secondLargestValue = GetSecondLargest(resultSQ[0:int(SamplingFrequency*0.001)])
            firstPeak = np.amax(resultSQ[0:int(SamplingFrequency)])
            peakToSecond =  10*np.log10(  firstPeak/secondLargestValue  )

            if peakToSecond > 3.2:
                print(' -> Possible Adquisition!')
                satellite.setAdquired(DopplerShift)
        

    outputSatellites = []
    for satellite in Satellites:
        if satellite.isAdquiered():
            outputSatellites.append(satellite)
    return outputSatellites

class GNSS_Satellite:

    def __init__(self, PRN_Number):
        self.PRN_Num = PRN_Number
        self.PRN_Code = GoldCode_Generator.generate(PRN_Number)

        self.Acquired = False
        self.MaxSNR = None
        self.DopplerHz = []
        self.CodePhaseSamples  = None
        CodePhaseChips = None

    def get_PRN_Num(self):
        return self.PRN_Num
    
    def get_PRN_Code(self):
        return self.PRN_Code

    def setAdquired(self, estimatedDopperShift):
        #Añadir aqui código para el estimated code shift
        self.Acquired = True
        self.DopplerHz.append(estimatedDopperShift)

    def isAdquiered(self):
        return self.Acquired
    

def GetSecondLargest(DataList):
    DataArray = np.array(DataList)

    Largest = np.amax(DataArray)
    LargestIndex = np.argmax(DataArray)
    
    ScaleAmount = 0.95
    ScaledLargest = ScaleAmount*Largest
    SecondLargest = 0
    SecondLargestIndex = 0

    for ind, val in enumerate(DataArray):
        if val < ScaledLargest:
            if val > SecondLargest:
            
                if np.abs(LargestIndex-ind) > 100:
                    SecondLargest = val
                    SecondLargestIndex = ind

    return SecondLargest
    



    
