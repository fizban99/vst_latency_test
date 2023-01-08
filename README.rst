vst_latency_test
################

This script tests the latency of a DAC/Audio Interface/Sound Card when using a midi keyboard with a vst instrument.
VST or VSTI are virtual instruments that you can use with your digital keyboard connected to the computer. Although you can use ASIO4ALL and your internal sound card, it is recommended to use an external sound card/audio interface that supports ASIO natively. For a nice playing experience, the time between pressing a key and hearing a sound should be minimal. This is called latency and should be less than 20ms in order not to interfere with the playing, although some players prefer values of less than 10ms. The best tool to test audio interface latencies is the RTL Utility (https://oblique-audio.com/rtl-utility.php) from Oblique Audio, but that assumes that the audio interface has both output and input. Some people, though, use DACs or USB cards without an input line and it is difficult to know the latency of those devices in this case. This script helps measuring that value and allows comparing it with other devices you might have.

Installation
############

1.- You need python 3.x installed
2.- Download the vst_latency_test.py script and requirements.txt or clone the repository
3.- In the install directory run `pip3 install -r requirements.txt`
4.- Download and install loopMIDI (https://www.tobias-erichsen.de/software/loopmidi.html). This is used to create a virtual MIDI port to emulate an external keyboard.
5.- Start your VST of preference. See below for free and easy options.


Free VSTs
#########

To play a virtual instrument you need the VST software and a host application that can communicate with it. One of the smallest hosts is nanoHost (https://www.tone2.com/nanohost.html). It is small, portable and free.
Once you have the host, you can choose from a myriad of VSTs. If you like the sound of the piano, 4FrontPiano (http://www.yohng.com/software/piano.html) is a free small VST with a nice sound and low on computer resources.
Another option is BassMidi VSTi from falcosoft (http://falcosoft.hu/softwares.html#bassmidi_vsti). This makes use of soundfonts. Some of the best free soundfonts can be found at Soundfonts4U (https://sites.google.com/site/soundfonts4u/)

