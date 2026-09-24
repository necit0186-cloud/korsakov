import io
import unittest
import urllib.error
from unittest.mock import patch

import server


class PublicFetchTest(unittest.TestCase):
    def test_retry_after_tls_handshake_timeout(self):
        with patch.object(server.urllib.request, "urlopen", side_effect=[
            urllib.error.URLError(TimeoutError("The handshake operation timed out")),
            io.BytesIO(b"page"),
        ]) as request, patch.object(server.time, "sleep"):
            self.assertEqual(server.fetch_text("https://t.me/channel"), "page")
            self.assertEqual(request.call_count, 2)

    def test_permanent_http_error_is_not_retried(self):
        error = urllib.error.HTTPError("https://t.me/channel", 404, "not found", {}, None)
        with patch.object(server.urllib.request, "urlopen", side_effect=error) as request:
            with self.assertRaisesRegex(RuntimeError, "HTTP 404"):
                server.fetch_text("https://t.me/channel")
            request.assert_called_once()


if __name__ == "__main__":
    unittest.main()
