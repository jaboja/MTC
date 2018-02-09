from datetime import datetime, time
from math import cos, sin
from numbers import Number
from pytz.tzinfo import BaseTzInfo, _notime
from pytz import open_resource, UTC

EPOCH_1900 = datetime(1900, 1, 1, tzinfo=UTC)
EPOCH_1970 = datetime(1970, 1, 1, tzinfo=UTC)


class LeapSeconds(object):
	_leap_seconds = None

	@classmethod
	def load(cls):
		with open_resource('leap-seconds.list') as f:
			table = [
				tuple(map(int, line.split(None, 2)[:2]))
				for line in f if not (
					line.startswith('#') or line.strip() == ''
				)
			]
		table.reverse()
		cls._leap_seconds = tuple(table)

	@classmethod
	def get_table(cls):
		if cls._leap_seconds is None:
			cls.load()
		return cls._leap_seconds

	@classmethod
	def at_date(cls, dt):
		delta = dt - EPOCH_1900
		s = delta.total_seconds()
		for (epoch, leap) in cls.get_table():
			if s >= epoch:
				break
		return leap


class martiandatetime(time):
	'''datetime.datetime equivalent for MTC'''

	def __new__(cls, sol=0, hour=0, minute=0, second=0, microsecond=0, tzinfo=None):
		"""Constructor.

		Arguments:

		sol, hour, minute (required)
		second, microsecond (default to zero)
		tzinfo (default to None)
		"""

		if not isinstance(sol, int):
			raise TypeError('int expected')

		if isinstance(hour, bytes):
			# Pickle (lack of) support
			raise NotImplementedError()

		if tzinfo is None:
			tzinfo = MTC()
		elif not isinstance(tzinfo, MTC):
			raise TypeError('tzinfo argument must be MTC')

		self = time.__new__(cls, hour, minute, second, microsecond)
		self._sol = sol
		self._tzinfo = tzinfo
		return self

	@property
	def sol(self):
		"""sol"""
		return self._sol

	def isoformat(self):
		raise TypeError('Martian time has no ISO format')

	def __str__(self):
		return 'Sol %d %.2d:%.2d:%.2d.%.6d MTC' % (
			self.sol, self.hour, self.minute, self.second, self.microsecond
		)

	__repr__ = __str__

	def __format__(self, fmt):
		if len(fmt) != 0:
			return self.strftime(fmt)
		return str(self)

	def _cmp(self, that, allow_mixed=False):
		assert isinstance(other, martiandatetime)
		return cmp(
			(self._sol, self._hour, self._minute, self._second, self._microsecond),
			(that._sol, that._hour, that._minute, that._second, that._microsecond)
		)

	def __hash__(self):
		"""Hash."""
		return hash((self._sol, self._hour, self._minute, self._second, self._microsecond))

	def strftime(self, fmt):
		raise NotImplementedError()
	def replace(self, *args, **kwargs):
		raise NotImplementedError()
	def _getstate(self):
		raise NotImplementedError()
	def __setstate(self, string, tzinfo):
		raise NotImplementedError()
	def __reduce__(self):
		raise NotImplementedError()



class MTC(BaseTzInfo):
	'''Coordinated Mars Time timezone'''
	_utcoffset = float('nan')
	_mtcoffset = 0
	_tzname = "MTC"
	zone = "MTC"

	def fromutc(self, dt, utc_offset=None):
		'''See datetime.tzinfo.fromutc

		utc_offset is difference between TT and UTC in seconds'''
		if dt.tzinfo and dt.tzinfo._utcoffset.seconds != 0:
			raise ValueError('fromutc: dt.tzinfo is not UTC')
		dt = dt.replace(tzinfo=UTC)

		if utc_offset is None:
			utc_offset = LeapSeconds.at_date(dt)
			utc_offset += 32.184  # TAI-UTC to TT-UTC

		s = (dt - EPOCH_1970).total_seconds()
		JDUT = s / 86400 + 2440587.5
		JDTT = JDUT - (utc_offset / 86400)
		return self.fromtt(JDTT)

	def fromtt(self, JDTT):
		'''Julian Date in Terrestial Time
		(i.e. number of days since January 1, 4713 BC (TT))
		to datetime in MTC. Based on:
		https://www.giss.nasa.gov/tools/mars24/help/algorithm.html'''
		if not isinstance(JDTT, Number):
			raise ValueError('fromtt: JDTT has to be a number')

		MTC = (JDTT - 2451549.5) / 1.0274912517 + 44796.0 - 9626E-7
		MTC += self._mtcoffset / 24.0
		hour = MTC % 1 * 24
		return martiandatetime(
			int(MTC),
			int(hour),
			int(hour * 60.0) % 60,
			int(hour * 36E2) % 60,
			int(hour * 36E8) % 1000000,
			self
		)

	def utcoffset(self, dt, is_dst=None):
		'''See datetime.tzinfo.utcoffset

		is_dst exists only to retain compatibility with DstTzInfo.
		'''
		raise TypeError('Martian time has no UTC offset. Use mtcoffset instead.')

	def mtcoffset(self, dt):
		'''utcoffset equivalent for Mars'''
		return self._mtcoffset

	def dst(self, dt, is_dst=None):
		'''See datetime.tzinfo.dst

		is_dst exists only to retain compatibility with DstTzInfo.
		'''
		return _notime

	def tzname(self, dt, is_dst=None):
		'''See datetime.tzinfo.tzname

		is_dst exists only to retain compatibility with DstTzInfo.
		'''
		return self._tzname

	def localize(self, dt, is_dst=False):
		'''Convert naive time to local time'''
		raise TypeError('Naive time cannot be converted to martian time')

	def normalize(self, dt, is_dst=False):
		'''Correct the timezone information on the given datetime.'''
		if isinstance(dt.tzinfo, MTC):
			return dt.replace(tzinfo=self)
		if dt.tzinfo is None:
			raise ValueError('Naive time - no tzinfo set')
		return self.fromutc(dt.astimezone(UTC))

	def __repr__(self):
		if self._mtcoffset:
			return '<MTC%+.2d>' % self._mtcoffset
		return '<MTC>'

	def __reduce__(self):
		raise NotImplementedError('MTC.__reduce__ not implemented')
