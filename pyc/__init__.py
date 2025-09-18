import struct
import marshal
import pyc.magic

# Subterranean blues

class PycHeader:
    def __init__(self):
        self.magic = 0
        self.bitfield = None
        self.timestamp = None
        self.filesize = None
        self.hash_val = None
        self.headersize = 12

    def get_magic(self):
        version = magic.MAGIC_TO_VERSION.get(self.magic)
        if version is None:
            version = magic.MAGIC_TO_VERSION.get(self.magic + 1)
        if version is None:
            raise Exception("Bad magic")
        return version

    def get_header(self):
        header = struct.pack("<I", self.magic)
        version = self.get_magic()

        if version < (3,3):  # Python ≤ 3.2
            header += struct.pack("<I", self.timestamp or 0)

        elif version <= (3,6):  # Python 3.3 – 3.6
            header += struct.pack("<I", self.bitfield)
            if self.bitfield == 0:
                header += struct.pack("<I", self.timestamp or 0)
            else:
                header += struct.pack("<I", self.hash_val or 0)

        else:  # Python ≥ 3.7
            header += struct.pack("<I", self.bitfield)
            if self.bitfield == 0:
                header += struct.pack("<II", self.timestamp or 0, self.filesize or 0)
            else:
                header += struct.pack("<Q", self.hash_val or 0)

        return header

    def analyze_header(self, header: bytes):
        self.magic, = struct.unpack_from("<I", header, 0)
        version = self.get_magic()

        if version < (3,3):
            self.headersize = 8
            self.timestamp, = struct.unpack_from("<I", header, 4)

        elif version <= (3,6):
            self.headersize = 12
            self.bitfield, val = struct.unpack_from("<II", header, 4)
            if self.bitfield == 0:
                self.timestamp = val
            else:
                self.hash_val = val

        else:
            self.headersize = 16
            self.bitfield, = struct.unpack_from("<I", header, 4)
            if self.bitfield == 0:
                self.timestamp, self.filesize = struct.unpack_from("<II", header, 8)
            else:
                (self.hash_val,) = struct.unpack_from("<Q", header, 8)
def get_code_info(data, header):
    marshalled = data[header.headersize:]
    code_object = marshal.loads(marshalled)

    return code_object
