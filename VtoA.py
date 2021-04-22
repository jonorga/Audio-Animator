# The purpose of this Python script is to animate the Z axis of an object with
# the values from the RMS volume

### Code units
# (1) Open WAV file - Complete
# (2) Read header for basic info (bit depth, samples, channels) - Complete
# (3) Use header info to loop read samples - Complete
# (4) Collect sample and find the RMS volume - Complete
## RMS = Square Root( (sample1^2 + sample2^2 + ... + sample300^2) / 300 )
# (5) Add RMS volume to list for info to be used in animation
# (6) Add the next sample to the front, once list is at 300, remove the last one from before
# (7) Adjust RMS value range to 0 to 100 ( new value = RMS value / (highest RMS value/100) )
# (8) Use loop to set object location on Z axis to new values, set key frame and move forward frames




from waveobject import waveObj



aud_file = waveObj('test.wav')
print(aud_file.sample_RMS(0))


