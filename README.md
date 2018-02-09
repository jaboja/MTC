# MTC
A Coordinated Mars Time (MTC) timezone for Python.

# Warning
This timezone is not 100% pytz compatible. Actually it is impossible to create a pytz timezone for other celestial body
as pytz assumes timezones to have some UTC offset and basically was designed for terrestial timezones. For that reason
some methods of martian time objects remain either unimplemented or returning dumb values (like NaN UTC offset*).
Nevertheless, it should be usable in most common use cases (like printing current time in some other place).

** I have introduced MTC offset instead. This way instead of meaningless values you get explicit error if you try to add UTC offset to MTC.*

# Usage

    from mtc import MTC
    from datetime import datetime

    new_zone = MTC()
    new_zone._mtcoffset = 15.08  # Olympus Mons is 226.2E
    
    print ('Current time atop Olympus Mons (MTC+15.08) is:\t%s'
        % new_zone.fromutc(datetime.utcnow()))


# Example

Run:

    python test.py

It should output current time on martian 0 meridian and the current time atop Olympus Mons (to show MTC offset usage).
