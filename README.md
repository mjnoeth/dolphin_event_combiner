# dolphin_event_combiner v1.0
Dolphin Version: 5.0.19.0
Meet Maestro:	 8.15.7

For swim teams using The Dolphin Timing system and Meet Maestro, this script is meant to assist
combining events. Our swim team is relatively small and often times relays can be combined to
save time during the meet. For example, if we have a Boy 9-10 relay with relay teams in lanes 1
and 2 and we have a Girls 9-10 relay with relay teams in lanes 3 and 4, then both these events
could be run at the same time. A pre-requisite is that the meet is setup to have the swimmers /
relay teams spread across different lanes. The Dolphin timing system is not aware of who should
be swimming where so if both the girls and boys swim at the same time and the timers collect
times then we will have a data file with times for lanes 1, 2, 3 and 4. If we import this file
into Meet Maestro for both the girls event AND the boys event then the appropriate times will
be populated.

# Usage
- Data Manager: Ensure that events / heats you want to combine do not have overlapping swimmers
- Starter: Starts the race normally
- Timers: Time the race normally
- Starter: Presses stop followed by reset normally
- Data Manager: Loads first event normally (will see "Loaded times for empty lanes X, Y, Z")
- Data Manager: Runs event combiner binary:

C:\CTSDolphin\meets\20240630-test>python c:\Users\test\dolphin_event_combiner\combine.py --directory ./
Using directory at './/'
Using current race '007_Event_1_Heat_1_Race_1_7_8_2024_11_7.csv'
Generating next race '007_Event_2_Heat_1_Race_2_7_8_2024_11_7.csv'

- Data Manager: Loads second event from copied file  (will see "Loaded times for empty lanes X, Y, Z")
- Starter / Data Manager advance event manually in Dolphin:
  - Starter presses start on starter
  - Someone on timer presses plunger to stop timing
  - Starter presses stop followed by reset
  - A file will be generated that will only have 1 time in it that can be ignored
- Data Manager: Confirm that we have advanced past the 2nd event we have combined

parameters:
-d | --directory: Dolphin data directory

# Dev notes
CurrentDolphinRace.txt contents:

6/30/2024 4:41:34 PM,6,5.0.19.0,2,2,1,2
<last update date> <last update time> <meet number> <dolphin version> <event> <event> <heat> <race>

Test usage:

C:\Users\test\dolphin_event_combiner>python combine.py  --directory test_event/
Using directory at 'test_event//'
Using current race '006_Event_15_Heat_3_Race_6_6_30_2024_17_49.csv'
Generating next race '006_Event_15_Heat_4_Race_7_6_30_2024_17_49.csv'

# Potential features and improvements
- Audit log: log in an append only file all the changes that are being made. This audit log
  should be created in the directory specified when the script runs.

