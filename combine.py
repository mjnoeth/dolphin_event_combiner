import argparse
from datetime import datetime
import glob
import os
import re
import shutil
import xmltodict
 

class CurrentSettings:
	def __init__(self, directory):
		current_settings_file = directory + 'CurrentSettings.xml'
		if not os.path.exists(current_settings_file):
			print(f"Error: CurrentSettings cannot find file '{current_settings_file}'")
			exit(-1)

		with open(current_settings_file) as f:
			xml_string = f.read()
			# Get rid of stupid version string.
			xml_string_array = xml_string.split("\n")
			xml_string = "\n".join(xml_string_array[1:])
			xml_dict = xmltodict.parse(xml_string)
			self.meet_number = xml_dict['Data']['General']['MeetNumber']


class CurrentRace:
	def __init__(self, directory):
		self.directory = directory
		current_race_file = directory + 'CurrentDolphinRace.txt'
		if not os.path.exists(current_race_file):
			print(f"Error: CurrentRace cannot find file '{current_race_file}'")
			exit(-1)

		with open(current_race_file) as f:
			race_string = f.read()
			race_string = re.sub(r"\s+", " ", race_string)
			race_array = race_string.split(",")
			if len(race_array) != 7:
				print(f"Error: CurrentRace has invalid file data: '{race_array}'")
			timestamp_string = race_array[0]
			format_string = "%m/%d/%Y %I:%M:%S %p"
			self.datetime = datetime.strptime(timestamp_string, format_string)

			self.meet_number = race_array[1]
			self.dolphin_version = race_array[2]
			self.event_1 = race_array[3]
			self.event_2 = race_array[4]
			self.heat = race_array[5]
			self.race = re.sub(r"\s+", "", race_array[6])

	def _Meet(self):
		return "{:03d}".format(int(self.meet_number))

	def _Event(self):
		return "Event_" + self.event_1

	def _Heat(self):
		return "Heat_" + self.heat

	def _Timestamp(self):
		return '{d.month}_{d.day}_{d.year}_{d.hour}_{d.minute}'.format(d=self.datetime)

	def _Race(self):
		return "Race_" + self.race

	def GetCurrentFilename(self):
		for filename in glob.glob(self.directory + "*"):
			if self._Timestamp() in filename:
				return os.path.basename(filename)
		print(f"Error: unable to find a race with '{self._Timestamp()}' contained within")
		exit(-1)

	def GetNextFilename(self):
		return self._Meet() + "_" + self._Event() + "_" + self._Heat() + "_" + self._Race() + "_" + self._Timestamp() + ".csv"
 

# Parse command line args.
parser = argparse.ArgumentParser(description="Dolphin timing system event combining script.")
parser.add_argument('-d', '--directory', help='Path to the Dolphin data directory')
args = parser.parse_args()

# Determine the Dolphin data directory we are working from.
if args.directory:
	directory = args.directory
else:
	directory = os.getcwd()
directory = directory + "/"
exists = os.path.exists(directory)
is_directory = os.path.isdir(directory)
is_writable = os.access(directory, os.W_OK)
if exists and is_directory and is_writable:
	print(f"Using directory at '{directory}'")
else:
	print(f"Error: directory at '{directory}' must exist, be a directory and be writable")
	print(f"exist: '{exists}' is_directory: '{is_directory}' is_writable: '{is_writable}'")
	exit(-1)

# Get the current settings.
current_settings = CurrentSettings(directory)

# Get the current race.
current_race = CurrentRace(directory)

# Get the latest race file generated.
current_filename = current_race.GetCurrentFilename()
print(f"Using current race '{current_filename}'")

# Get the filename of the next race.
next_filename = current_race.GetNextFilename()
print(f"Generating next race '{next_filename}'")
next_filename_fullpath = directory + next_filename
if os.path.exists(next_filename_fullpath):
    print(f"Error: The generated file already exists '{next_filename_fullpath}'")

# Copy the file
current_filename_fullpath = directory + current_filename
shutil.copyfile(current_filename_fullpath, next_filename_fullpath)
