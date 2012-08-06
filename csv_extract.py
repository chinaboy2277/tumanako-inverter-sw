# Lachlan Rhodes 2012 <rhodes.lachlan@gmail.com>
# Written for Tumanako Project
# Software for extracting data from data dumps for motor testing

# Importing files
import os
import sys
import csv

# Extracting data for
# Bus (V)
# Brake
# RPM
# Phase 1 (A)
# Phase 2 (A)
# Phase 3 (A)
# Bus (A)
# Flux Angle
# Electric Angle
# Direction
# RawAccelPOT
# Flux In
# Flux Out (Id)
# Flux Vd
# pwrStgTemp (C)
# Motor Temp (C)
# Loop time (ms)
# PhAOffset (A)
# PhBOffset (A)
# Total (A)
# SlipFreq
# RunTime (sec)
# RotorTimeConst
# Regen
# Torque Limit
# Torque In
# Torque Out(Iq)
# Torque Vq

if (len(sys.argv) == 0):
	print("Error: Please indicate a file to extract from")
	sys.exit()
elif (len(sys.argv) > 2):
	print("Error: Too many inputs indicated, please indicate only the file to work with")
	sys.exit()

filename = sys.argv[1] #Recording the filename (may use it to create extract name)

#Psuedo Code

#Find 'BUS' to begin
#Collect all values till end
#Convert to values
#Place in csv file
#Loop back

row = 1 # for counting lines of data, useful for killing at end
batch = 1 #counts total number of batches analysed
exit_out = 0 # really dodgy boolean value, to help with killing
data_file = open(filename)
tot_rows = len(data_file.readlines()) #getting total number of lines, which will help ensure the loop ends properly

data_file = open(filename) #reopening file so it returns back to start

filename=filename[0:len(filename)-4] #removing .txt from end
cur_dir = os.getcwd()

#Creating new csv file, appending first row with titles
target = open(filename+".csv","w")
wr = csv.writer(target, dialect='excel')
wr.writerow(["Bus (V)", "Brake", "RPM", "Phase 1 (A)", "Phase 2 (A)", "Phase 3 (A)", "Bus (A)", "FluxAngle", "Electric Angle", "Direction", "RawAccelPOT", "FluxIn", "FluxOut (Id)", "Flux Vd", "pwrStgTemp (C)", "motorTemp (C)", "Loop time (ms)", "PhAOffset (A)", "PhBOffset (A)", "Total (A)", "SlipFreq", "RunTime (sec)", "RotorTimeConst", "Regen", "Torque Limit", "Torque In", "Torque Out(Iq)", "Torque Vq"])

#Conducting initial scan for first line of data
line = data_file.readline()

while row < tot_rows:
	
	while (line[7:10] != 'Bus'):
		line = data_file.readline()
		row = row+1
		if row > tot_rows:
			exit_out = 1
			break
	if exit_out == 1:
		break
	
	
	#First line
	busv = int(line[line.index(':')+1:line.index('p')-1])
	pwrstgtemp = int(line[line.index('p')+15:len(line)-1])
	
	
	#line 2
	line = data_file.readline()
	row = row+1
	if line[19:21] == 'ON': #running check as basic 1/0
		brake = 1
	else:
		brake = 0
	motortemp = int(line[line.index('m')+14:len(line)-1])
	
	
	#line 3
	row = row+1
	line = data_file.readline()
	rpm = int(line[line.index(':')+1:line.index('L')-1])
	looptime = int(line[line.index('L')+15:len(line)-1])
	
	
	#line 4
	line = data_file.readline()
	row = row+1
	phase1 = int(line[line.index(':')+1:line.index('PhA')-1])
	phaoffset = int(line[line.index('PhA')+14:len(line)-1])
	
	
	#line 5
	line = data_file.readline()
	row = row+1
	phase2 = int(line[line.index(':')+1:line.index('PhB')-1])
	phboffset = int(line[line.index('PhB')+14:len(line)-1])
	
	
	#line 6
	line = data_file.readline()
	row = row+1
	phase3 = int(line[line.index(':')+1:line.index('T')-1])
	total = float(line[line.index('T')+10:len(line)-1])
	
	
	#line 7
	line = data_file.readline()
	row = row+1
	busa = int(line[line.index(':')+1:line.index('Sl')-1])
	slipfreq = int(line[line.index('Sl')+9:len(line)-1])
	
	
	#line 8
	line = data_file.readline()
	row = row+1
	fluxangle = int(line[line.index(':')+1:line.index('R')-1])
	runtime = int(line[line.index('R')+14:len(line)-1])
	
	
	#line 9
	line = data_file.readline()
	row = row+1
	electricangle = int(line[line.index(':')+1:line.index('R')-1])
	rotortimeconst = int(line[line.index('R')+15:len(line)-1])
	
	
	#line 10
	line = data_file.readline()
	row = row+1
	direction = int(line[16:21])
	if line[len(line)-2:len(line)] == 'ff': #running check as basic 1/0
		regen = 1
	else:
		regen = 0
	
	
	#line 11
	line = data_file.readline()
	row = row+1
	rawaccelpot = int(line[line.index(':')+1:line.index('Tor')-1])
	if line[len(line)-2:len(line)] == 'ff': #running check as basic 1/0
		torquelim = 1
	else:
		torquelim = 0
	
	#line 12
	line = data_file.readline()
	row = row+1
	fluxin = int(line[line.index(':')+1:line.index('T')-1])
	torquein = int(line[line.index('T')+10:len(line)-1])
	
	#line 13
	line = data_file.readline()
	row = row+1
	fluxout = int(line[line.index(':')+1:line.index('T')-1])
	torqueout = int(line[line.index('T')+15:len(line)-1])
	
	#line 14
	line = data_file.readline()
	row = row+1
	fluxvd = int(line[line.index(':')+1:line.index('T')-1])
	torquevq = int(line[line.index('T')+10:line.index('T')+16])
	
	
	#all values aquired for this row, now to place them in a new csv file
	wr.writerow([busv, brake, rpm, phase1, phase2, phase3, busa, fluxangle, electricangle, direction, rawaccelpot, fluxin, fluxout, fluxvd, pwrstgtemp, motortemp, looptime, phaoffset, phboffset, total, slipfreq, runtime, rotortimeconst, regen, torquelim, torquein, torqueout, torquevq])
	
	batch = batch + 1
	
#Closing document
print("Complete! Analysed a total of ",batch," batches of data")
target.close()
