# The purpose of this Python script is to animate the Z axis of an object with
# the values from the RMS volume

### Code units
# (1) Open WAV file - Complete
# (2) Read header for basic info (bit depth, samples, channels) - Complete
# (3) Use header info to loop read samples - Complete
# (4) Collect sample and find the RMS volume - Complete
## RMS = Square Root( (sample1^2 + sample2^2 + ... + sample300^2) / 300 )
# (5) Get total length in frame of Audio file - Complete
# (6) Clamp range of RMS values based on bit depth to range specified as variable - Complete
# (7) Animate to relevant keyframes with values from Audio file




from waveobject import waveObj



aud_file = waveObj('test3.wav')
min_val = 0
max_val = 30

i = 0
while i < aud_file.length_of_data("frames"):
	# The next line prints the Z value at each frame
	print(aud_file.decibel_raw(aud_file.sample_at_frame(i), 0.001))
	i += 1
