PG 1  LB SU      ' start here on powerupEM=2       ' turn off promptPR         ' print newline for scanimageA=750000   ' accelerationD=5000000  ' decelerationP=0        ' positionD1=20      ' input 1 debounce to 20msecH 1200     ' wait for calibrationLB G1      ' infinite loop begins hereS1=5,0,1  ' halt if paper present' scanbarVM=138000MA -1270000H 3250' fast to slotsVM=600000MA -1070000H 800' slow over slotsVM=300000MA -1270000H' page turnVM=65000MA 0H 3700S1=0,1,1  ' ignore sensor state' page splitVM=300000MA 0H 1000S1=5,1,1  ' halt if paper absent' fast to the startVM=600000MA 0H 100S1=0,1,1  ' ignore sensor state' fast to the startVM=600000MA 0HPR  ' print newline for scanimageBR G1EPG