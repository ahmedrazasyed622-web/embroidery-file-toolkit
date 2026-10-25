import tempfile
import unittest
from pathlib import Path

from embroidery_info import identify_format, read_dst_info


class EmbroideryInfoTests(unittest.TestCase):

    def test_identify_dst_format(self):
        self.assertEqual(
            identify_format("design.dst"),
            "Tajima DST"
        )

    def test_identify_pes_format(self):
        self.assertEqual(
            identify_format("design.pes"),
            "Brother PES"
        )

    def test_read_dst_information(self):
        header = (
            "LA:TEST\r"
            "ST:0000003\r"
            "CO:001\r"
            "+X:00100\r"
            "-X:00020\r"
            "+Y:00050\r"
            "-Y:00010\r"
        ).encode("ascii")

        header = header.ljust(512, b" ")

        body = (
            b"\x00\x00\x03"
            b"\x00\x00\x83"
            b"\x00\x00\xC3"
            b"\x00\x00\xF3"
        )

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "sample.dst"
            path.write_bytes(header + body)

            info = read_dst_info(path)

            self.assertEqual(info["width_mm"], 12.0)
            self.assertEqual(info["height_mm"], 6.0)
            self.assertTrue(info["end_marker_found"])


if __name__ == "__main__":
    unittest.main()
