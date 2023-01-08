# -*- coding: utf-8 -*-
from mido import open_output, Message
import time
import sounddevice as sd
# from scipy.io.wavfile import write
import numpy as np
import pyprind
import argparse
import sys

def print_names(wasapi_input_devices):
    names = (device["name"] for device in wasapi_input_devices )
    print("Available devices: ")
    print ("\n".join(names))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    #usage="%(prog) recording_device",
    description='\r\n'.join(["sends a midi note to 'loopMIDI Port 1' and measures ",
                 "the latency of the signal recording the sound through another",
                 "device"])
    )

   
    parser.add_argument('recording_device', metavar='recording_device', type=str,
                   help='any part of the name of the recording device')
    

    args = parser.parse_args()
    
    devices = sd.query_devices()
    wasapi_input_devices = []
    for device in devices:
        if device["hostapi"]==3 and device["max_input_channels"]>0:
                wasapi_input_devices.append(device)
                
    if "recording_device" not in args:
        parser.print_help()
        print_names(wasapi_input_devices)
        sys.exit()
    
    device_name = args.recording_device.lower()   
    
    seconds = 1  # Duration of recording

    for device in wasapi_input_devices:
        if device_name.lower() in device["name"].lower():
            print(f"Selected device:  {device['name']}")
            input_device = device["index"]
            break
    else:
        print("No device name match found")
        print_names(wasapi_input_devices)
        sys.exit()
            
    input_device =38
    output_device = sd.default.device[1]
    sd.default.device = (input_device, output_device)
    device = sd.query_devices()[input_device]
    channels = device["max_input_channels"]
    fs = int(device["default_samplerate"])
    sd.default.latency = 'low'
    
    n_tests = 10
    print("Sending midi notes through 'loopMIDI Port 1'...", flush=True)
    bar = pyprind.ProgBar(n_tests, bar_char='█',title='Progress',monitor=False)
    samples_sum = 0
    latency_sum = 0
    
    for n_test in range(1,n_tests+1):
        myrecording = sd.rec(int(seconds * fs), 
                             samplerate=fs, 
                             channels=channels)
        outport = open_output('loopMIDI Port 1')
        
        
        msg1 = Message('note_on', note=100, velocity=127, time=0)
        outport.send(msg1)
        time.sleep(.5)
        msg1 = Message('note_on', note=100, velocity=0, time=0)
        outport.send(msg1)
    
        outport.close()
        
    
        sd.wait()  # Wait until recording is finished
    
        samples = 99999
        threshold = np.max(np.abs(myrecording))/10
        if threshold > .0003:
            if myrecording.shape[1]==1:
              # duplicate mono channel
              myrecording = np.tile(myrecording, (1, 2))  
            for i in range(myrecording.shape[0]-1):
                if ((abs(myrecording[i][0]) > threshold or abs(myrecording[i][1]) > threshold) and 
                    (abs(myrecording[i+1][0]) > threshold or abs(myrecording[i+1][1]) > threshold)) :
                    samples = i
                    break
            latency = 1/fs*samples*1000
            latency_sum += latency
            samples_sum += samples
            bar.update(item_id=f"{samples_sum/n_test:.0f} samples {(latency_sum/n_test):.1f} ms")
        else:
            print (f"Nothing was recorded. Check your cable or vst player settings")
            break
        sd.stop()
    if samples != 99999:
        print (f"\nlatency in samples: {samples_sum/n_tests:.0f} ({latency_sum/n_tests:.1f} ms)")
    # write('output.wav', fs, myrecording)  # Save as WAV file 
