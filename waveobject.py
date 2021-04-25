import struct
import math

class waveObj:
	def __init__(self, wave_file):
		# Read audio file
		audio_file = open(wave_file, 'rb')
		self.raw_audio_data = audio_file.read()

		# Header variables
		file_format = chr(4)
		file_format = self.raw_audio_data[0:4]
		self.file_format = file_format.decode('ascii') # RIFF spec

		total_size_en = bytes(4)
		total_size_en = self.raw_audio_data[4:8]
		self.total_size = int.from_bytes(total_size_en, byteorder='little') # Total file size minus 8 bytes

		format_type = chr(4)
		format_type = self.raw_audio_data[8:12]
		self.format_type = format_type.decode('ascii') # WAVE spec

		chunk1_header = chr(4)
		chunk1_header = self.raw_audio_data[12:16]
		self.chunk1_header = chunk1_header.decode('ascii') # Chunk 1 header (expected "fmt ")

		chunk1_size_en = bytes(4)
		chunk1_size_en = self.raw_audio_data[16:20]
		self.chunk1_size = int.from_bytes(chunk1_size_en, byteorder='little') # Chunk 1 size (not including this or header)

		audio_format_en = bytes(2)
		audio_format_en = self.raw_audio_data[20:22]
		self.audio_format = int.from_bytes(audio_format_en, byteorder='little') # 1 is PCM, others are compressed

		num_of_channels_en = bytes(2)
		num_of_channels_en = self.raw_audio_data[22:24]
		self.num_of_channels = int.from_bytes(num_of_channels_en, byteorder='little') # Number of channels

		sample_rate_en = bytes(4)
		sample_rate_en = self.raw_audio_data[24:28]
		self.sample_rate = int.from_bytes(sample_rate_en, byteorder='little') # Sample rate

		byte_rate_en = bytes(4)
		byte_rate_en = self.raw_audio_data[28:32]
		self.byte_rate = int.from_bytes(byte_rate_en, byteorder='little') # Sample rate * Bytes/sample * Channels

		block_line_en = bytes(2)
		block_line_en = self.raw_audio_data[32:34]
		self.block_line = int.from_bytes(block_line_en, byteorder='little') # Number of channels * Bytes/sample

		bits_per_samples_en = bytes(2)
		bits_per_samples_en = self.raw_audio_data[34:36]
		self.bits_per_samples = int.from_bytes(bits_per_samples_en, byteorder='little') # Bits per samples

		chunk2_header = chr(4)
		chunk2_header = self.raw_audio_data[36:40]
		self.chunk2_header = chunk2_header.decode('ascii') # Chunk 2 header

		chunk2_size_en = bytes(4)
		chunk2_size_en = self.raw_audio_data[40:44]
		self.chunk2_size = int.from_bytes(chunk2_size_en, byteorder='little') # Chunk 2 size

		


	def sample_raw(self, index_pos): # Index position in the list of samples
		bit_depth = int(self.block_line/self.num_of_channels)
		sample_value_en = bytes(bit_depth)
		index_pos += 44
		sample_value_en = self.raw_audio_data[index_pos:index_pos+bit_depth]
		return int.from_bytes(sample_value_en, byteorder='little')

	def sample_RMS(self, index_pos, milliseconds): # Index position in the list of samples
		counter = index_pos
		rms_length = 0 # counter to limit calculation to samples in time length
		samples_in_time = self.sample_rate * milliseconds # total number of samples to be considered (if avail)
		rms_val = 0
		while counter >= 0 and rms_length < samples_in_time:
			rms_val += self.sample_raw(counter) ** 2
			counter -= 1
			rms_length += 1
		rms_val /= samples_in_time
		return int(math.sqrt(rms_val))
		# take square root of RMS value

	def decibel_raw(self, index_pos, milliseconds):
		return math.log(self.sample_RMS(index_pos, milliseconds)/(2 ** self.bits_per_samples), 10)

	def decibel_RMS_clamped(self, index_pos, milliseconds, min_val, max_val):
		temp = self.decibel_RMS(index_pos, milliseconds)

	def sample_at_frame(self, frame, frame_rate = 24): # Frame: frame to find sample at, Frame Rate: frame rate of video for reference
		pos = frame/frame_rate
		sample = int(pos*self.sample_rate)
		return sample

	def frame_at_sample(self, sample, frame_rate = 24): # Sample: sample to find frame at, Frame Rate: frame rate of video for reference
		pos = sample/self.sample_rate
		frame = int(pos*frame_rate)
		return frame

	def RMS_at_frame(self, frame, frame_rate = 24): # Frame to find sample RMS value at, Frame Rate: frame rate of video for reference
		return self.sample_RMS(self.sample_at_frame(frame, frame_rate))

	def length_of_data(self, data_type, frame_rate = 24): # Return the length of data of the specified type (bytes, samples, milliseconds, frames)
		if data_type == "bytes":
			return self.chunk2_size
		elif data_type == "samples":
			return self.chunk2_size/self.block_line
		elif data_type == "milliseconds":
			return (self.chunk2_size/self.block_line)/self.sample_rate
		elif data_type == "frames":
			return int(((self.chunk2_size/self.block_line)/self.sample_rate)*frame_rate)
		else:
			return "Invalid data type"


	def sample_RMS_clamped(self, index_pos, milliseconds, min_val, max_val): # Return RMS value clamped to min/max range.
		temp = self.sample_RMS(index_pos, milliseconds)/ (2 ** self.bits_per_samples)
		return round((temp * max_val) + min_val, 4)

	def sample_raw_clamped(self, index_pos, min_val, max_val): # Return RMS value clamped to min/max range.
		temp = self.sample_raw(index_pos)/ (2 ** self.bits_per_samples)
		return round((temp * max_val) + min_val, 4)
		
