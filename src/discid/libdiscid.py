# Copyright (C) 2013  Johannes Dewender
# Copyright (C) 2022  Cube
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Please submit bug reports to GitHub:
# https://github.com/JonnyJD/python-discid/issues
#
# Some parts of the source code have been modified by Cube to differ from the original.
# The modified portions are explicitly disclosed in accordance with GNU LESSER GENERAL PUBLIC LICENSE Version 3.
"""libdiscid dynamic loading code and constants

The code that works with Disc objects is in disc.py
"""

import os
import sys
import ctypes
from ctypes import c_void_p, c_char_p

from discid.util import _encode, _decode

# Unlike the original, the modified source code specifies the .dll directly.
_LIB = ctypes.cdll.LoadLibrary(os.getcwd() + '/discid.dll')

try:
    _LIB.discid_get_version_string.argtypes = ()
    _LIB.discid_get_version_string.restype = c_char_p
except AttributeError:
    pass
def _get_version_string():
    """Get the version string of libdiscid
    """
    try:
        version_string = _LIB.discid_get_version_string()
    except AttributeError:
        return "libdiscid < 0.4.0"
    else:
        return _decode(version_string)

_LIB.discid_get_default_device.argtypes = ()
_LIB.discid_get_default_device.restype = c_char_p
def get_default_device():
    """The default device to use for :func:`read` on this platform
    given as a :obj:`unicode` or :obj:`str <python:str>` object.
    """
    device = _LIB.discid_get_default_device()
    return _decode(device)

try:
    _LIB.discid_get_feature_list.argtypes = (c_void_p, )
    _LIB.discid_get_feature_list.restype = None
except AttributeError:
    _features_available = False
else:
    _features_available = True
def _get_features():
    """Get the supported features for the platform.
    """
    features = []
    if _features_available:
        c_features = (c_char_p * 32)()
        _LIB.discid_get_feature_list(c_features)
        for feature in c_features:
            if feature:
                features.append(_decode(feature))
    else:
        # libdiscid <= 0.4.0
        features = ["read"]     # no generic platform yet
        try:
            # test for ISRC/MCN API (introduced 0.3.0)
            _LIB.discid_get_mcn
        except AttributeError:
            pass
        else:
            # ISRC/MCN API found -> libdiscid = 0.3.x
            if (sys.platform.startswith("linux") and
                    not os.path.isfile("/usr/lib/libdiscid.so.0.3.0")
                    and not os.path.isfile("/usr/lib64/libdiscid.so.0.3.0")):
                features += ["mcn", "isrc"]
            elif sys.platform in ["darwin", "win32"]:
                features += ["mcn", "isrc"]

    return features

LIBDISCID_VERSION_STRING = _get_version_string()

FEATURES = _get_features()


# vim:set shiftwidth=4 smarttab expandtab:
