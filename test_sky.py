import unittest
import xml.etree.ElementTree as ET

from sky import sky


class SkyTests(unittest.TestCase):
    def test_same_seed_same_sky(self):
        self.assertEqual(sky("hello"), sky("hello"))

    def test_different_seed_different_sky(self):
        self.assertNotEqual(sky("hello"), sky("goodbye"))

    def test_valid_svg_and_dimensions(self):
        root = ET.fromstring(sky("aster", 640, 240))
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertEqual(root.attrib["viewBox"], "0 0 640 240")
        self.assertEqual(len(root.findall(".//{http://www.w3.org/2000/svg}circle")), 85)

    def test_rejects_unreasonable_dimensions(self):
        with self.assertRaises(ValueError):
            sky("aster", 0, 240)


if __name__ == "__main__":
    unittest.main()
