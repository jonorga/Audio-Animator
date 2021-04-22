# The purpose of this Python script is to animate the Z axis of an object with
# the values from the RMS volume

### Code units
# (1) Open WAV file
# (2) Read header for basic info (bit depth, samples, channels)
# (3) Use header info to loop read samples
# (4) Collect sample and find the RMS volume
## RMS = Square Root( (sample1^2 + sample2^2 + ... + sample300^2) / 300 )
# (5) Add RMS volume to list for info to be used in animation
# (6) Add the next sample to the front, once list is at 300, remove the last one from before
# (7) Adjust RMS value range to 0 to 100 ( new value = RMS value / (highest RMS value/100) )
# (8) Use loop to set object location on Z axis to new values, set key frame and move forward frames



import struct


### ====== Unit 1 - Open file ======

# Open and read file
audio_file = open('test.wav', 'rb')
raw_audio_data = audio_file.read()


### ====== Unit 2 - Read header ======

# Header data variables
file_format = chr(4)
file_format = raw_audio_data[0:4]
file_format = file_format.decode('ascii')

total_size = bytes(4)
total_size = raw_audio_data[4:8]
total_size_dc = int.from_bytes(total_size, byteorder='little')

format_type = chr(4)
format_type = raw_audio_data[8:12]
format_type = format_type.decode('ascii')

chunk1_header = chr(4)
chunk1_header = raw_audio_data[12:16]
chunk1_header = chunk1_header.decode('ascii')

chunk1_size = bytes(4)
chunk1_size = raw_audio_data[16:20]
chunk1_size_dc = int.from_bytes(chunk1_size, byteorder='little')

audio_format = bytes(2)
audio_format = raw_audio_data[20:22]
audio_format_dc = int.from_bytes(audio_format, byteorder='little')

num_of_channels = bytes(2)
num_of_channels = raw_audio_data[22:24]
num_of_channels_dc = int.from_bytes(num_of_channels, byteorder='little')

sample_rate = bytes(4)
sample_rate = raw_audio_data[24:28]
sample_rate_dc = int.from_bytes(sample_rate, byteorder='little')

byte_rate = bytes(4)
byte_rate = raw_audio_data[28:32]
byte_rate_dc = int.from_bytes(byte_rate, byteorder='little')

block_line = bytes(2)
block_line = raw_audio_data[32:34]
block_line_dc = int.from_bytes(block_line, byteorder='little')

bits_per_samples = bytes(2)
bits_per_samples = raw_audio_data[34:36]
bits_per_samples_dc = int.from_bytes(bits_per_samples, byteorder='little')

chunk2_header = chr(4)
chunk2_header = raw_audio_data[36:40]
chunk2_header = chunk2_header.decode('ascii')

chunk2_size = bytes(4)
chunk2_size = raw_audio_data[40:44]
chunk2_size_dc = int.from_bytes(chunk2_size, byteorder='little')


#print sec
print(file_format) # RIFF spec
print(total_size_dc) # Total file size minus 8 bytes
print(format_type) # WAVE spec
print(chunk1_header) # Chunk 1 header (expected "fmt ")
print(chunk1_size_dc) # Chunk 1 size (not including this or header)
print(audio_format_dc) # 1 is PCM, others are compressed
print(num_of_channels_dc) # Number of channels
print(sample_rate_dc) # Sample rate
print(byte_rate_dc) # Sample rate * Bytes/sample * Channels
print(block_line_dc) # Number of channels * Bytes/sample
print(bits_per_samples_dc) # Bits per samples
print(chunk2_header) # Chunk 2 header
print(chunk2_size_dc) # Chunk 2 size


