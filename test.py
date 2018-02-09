from mtc import MTC
from datetime import datetime


new_zone = MTC()
utc_time = datetime.utcnow()

print (
	'Current MTC time:\n\t%s'
	% new_zone.fromutc(utc_time)
)

new_zone._mtcoffset = 15.08  # Olympus Mons is 226.2E
print (
	'\nCurrent time atop Olympus Mons (MTC+15.08):\t%s'
	% new_zone.fromutc(utc_time)
)

print (
	'\nThere is no one on the whole planet and the red world lasts in a perpetual peace.'
)
