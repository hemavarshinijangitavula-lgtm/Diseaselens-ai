import os
import unittest
from unittest.mock import patch

from app.fire_service import parse_hotspot_csv, get_fire_hotspots, FirmsConfigError

SAMPLE_CSV = '''latitude,longitude,bright_ti4,frp,confidence,satellite,instrument,acq_date,acq_time,daynight
13.4,78.6,330.2,7.1,high,N20,VIIRS,2026-11-23,1020,D
invalid,78.5,333.0,4.2,low,N20,VIIRS,2026-11-23,1021,N
'''

class FireServiceTests(unittest.TestCase):
    def test_csv_parser_normalizes_valid_row_and_skips_invalid_coordinates(self):
        rows = parse_hotspot_csv(SAMPLE_CSV)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["latitude"], 13.4)
        self.assertEqual(rows[0]["longitude"], 78.6)
        self.assertEqual(rows[0]["frp"], 7.1)
        self.assertEqual(rows[0]["satellite"], "N20")

    def test_missing_key_raises_configuration_error(self):
        with patch.dict(os.environ, {"NASA_FIRMS_MAP_KEY": ""}):
            with self.assertRaises(FirmsConfigError):
                get_fire_hotspots(78, 13, 79, 14)

    def test_invalid_source_rejected(self):
        with patch.dict(os.environ, {"NASA_FIRMS_MAP_KEY": "dummy_key"}):
            with self.assertRaises(ValueError):
                get_fire_hotspots(78, 13, 79, 14, 1, "UNKNOWN_SOURCE")

if __name__ == "__main__":
    unittest.main()
