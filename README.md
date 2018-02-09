# MTC
A Coordinated Mars Time (MTC) timezone for Python.

# Warning
This timezone is not 100% pytz compatible. Actually it is impossible to create a pytz timezone for other celestial body
as pytz assumes timezones to have some UTC offset (read: it was designed for terrestial timezones).
Also pytz timezones return date-time as the `datetime` objects which have strict limit on months not exceeding 12.
As Martian time does not and can not (for obvious reasons) use terrestial calendar, I decided to create
a new `martiandatetime` class which mimics `datetime`, but is not instance of it. Also, for above reasons
some methods of `martiandatetime` objects either remain unimplemented or return dumb values (like NaN UTC offset).
Nevertheless, it should be usable in common use cases (like printing current local time on Mars).

By the way, UTC offset is NaN yet I have introduced MTC offset instead,
so you shall get explicit error if you try to add UTC offset to MTC (which is meaningless).

This class does not implement any calendar. The date is reduced to sol number.

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
