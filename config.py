import os
from pathlib import Path

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)))

GCODE_TEMP_PATH = Path(BASE, 'tmp')
GCODE_COMPRESSOR_WIN = Path(BASE, 'VC_compress_gcode.exe')
GCODE_COMPRESSOR_MAC = Path(BASE, 'VC_compress_gcode_MAC')
GCODE_TEMP_PATH.mkdir(exist_ok=True)