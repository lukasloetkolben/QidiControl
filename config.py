import os
from pathlib import Path

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)))

GCODE_TEMP_PATH = BASE
GCODE_COMPRESSOR_WIN = Path(BASE, 'VC_compress_gcode.exe')
GCODE_COMPRESSOR_MAC = Path(BASE, 'VC_compress_gcode_MAC')
