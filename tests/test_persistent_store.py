import os
import unittest
from pathlib import Path
from unittest.mock import patch

import persistent_store as store


class PersistentStoreTest(unittest.TestCase):
    def setUp(self):
        self.values = {}
        self.environment = patch.dict(os.environ, {
            "KV_REST_API_URL": "https://example.upstash.io",
            "KV_REST_API_TOKEN": "test-token",
        })
        self.environment.start()
        self.client = patch.object(store, "redis", side_effect=self.command)
        self.client.start()

    def tearDown(self):
        self.client.stop()
        self.environment.stop()

    def command(self, action, *args):
        key = args[0]
        if action == "GET":
            return self.values.get(key)
        if action == "EXISTS":
            return int(key in self.values)
        if action == "SET":
            if "NX" in args and key in self.values:
                return None
            self.values[key] = args[1]
            return "OK"
        if action == "DEL":
            return int(self.values.pop(key, None) is not None)
        if action == "EVAL":
            _, key_count, key, owner = args
            if key_count == 1 and self.values.get(key) == owner:
                del self.values[key]
                return 1
            return 0
        raise AssertionError(action)

    def test_durable_documents_and_sessions(self):
        path = Path(store.__file__).parent / "data" / "users.json"
        self.assertFalse(store.exists(path))
        with self.assertRaises(FileNotFoundError):
            store.read_json(path)
        self.assertTrue(store.write_json(path, {"id": "saved"}, only_if_missing=True))
        self.assertFalse(store.write_json(path, {"id": "lost"}, only_if_missing=True))
        self.assertEqual(store.read_json(path), {"id": "saved"})
        store.save_session("secret-cookie", "user-1")
        self.assertEqual(store.get_session("secret-cookie"), "user-1")
        self.assertNotIn("secret-cookie", " ".join(self.values))
        store.delete_session("secret-cookie")
        self.assertIsNone(store.get_session("secret-cookie"))

    def test_lock_releases_after_error(self):
        lock = store.StoreLock("test")
        with self.assertRaises(ValueError):
            with lock:
                self.assertIn("korsakov:lock:test", self.values)
                raise ValueError("failed write")
        self.assertNotIn("korsakov:lock:test", self.values)

    def test_incomplete_credentials_fail_closed(self):
        with patch.dict(os.environ, {"KV_REST_API_TOKEN": "", "UPSTASH_REDIS_REST_TOKEN": ""}):
            with self.assertRaises(RuntimeError):
                store.read_json(Path(store.__file__).parent / "data" / "users.json")


if __name__ == "__main__":
    unittest.main()
