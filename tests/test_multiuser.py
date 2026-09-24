import http.client
import json
import tempfile
import threading
import unittest
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

import server


class MultiuserTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.old = {name: getattr(server, name) for name in ('DATA_DIR', 'ACCOUNT_FILE', 'CONNECTIONS_FILE', 'RUNTIME_FILE', 'USERS_FILE', 'FOLDERS_FILE', 'FOLDER_DIR')}
        server.DATA_DIR = root
        for name, filename in [('ACCOUNT_FILE', 'account.json'), ('CONNECTIONS_FILE', 'connections.json'), ('RUNTIME_FILE', 'runtime.json'), ('USERS_FILE', 'users.json'), ('FOLDERS_FILE', 'folders.json')]:
            setattr(server, name, root / filename)
        server.FOLDER_DIR = root / 'folders'
        server.SESSIONS.clear()
        salt, digest = server.password_hash('old-password')
        server.write_secure_json(server.ACCOUNT_FILE, {'name': 'Owner', 'email': 'necit0186@gmail.com', 'salt': salt, 'password_hash': digest})
        server.write_secure_json(server.CONNECTIONS_FILE, {'vk': {'url': 'https://vk.ru/old', 'token': 'old-secret', 'webhook_secret': 'secret'}})
        server.write_secure_json(server.RUNTIME_FILE, {'platforms': {}, 'snapshots': [], 'events': []})
        server.migrate_legacy()
        self.http = ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
        self.thread = threading.Thread(target=self.http.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.http.shutdown()
        self.http.server_close()
        self.thread.join()
        for name, value in self.old.items():
            setattr(server, name, value)
        server.SESSIONS.clear()
        self.temp.cleanup()

    def request(self, path, payload=None, cookie=None):
        conn = http.client.HTTPConnection('127.0.0.1', self.http.server_port)
        headers = {'Content-Type': 'application/json'}
        if cookie:
            headers['Cookie'] = cookie
        conn.request('POST' if payload is not None else 'GET', path, json.dumps(payload) if payload is not None else None, headers)
        res = conn.getresponse()
        body = json.loads(res.read())
        result = (res.status, body, (res.getheader('Set-Cookie') or '').split(';')[0])
        conn.close()
        return result

    def test_migration_registration_and_permissions(self):
        status, _, owner_cookie = self.request('/api/auth/login', {'email': 'necit0186@gmail.com', 'password': 'old-password'})
        self.assertEqual(status, 200)
        _, data, _ = self.request('/api/folders', cookie=owner_cookie)
        legacy_id = data['folders'][0]['id']
        self.assertEqual(server.load_connections(legacy_id)['vk']['token'], 'old-secret')
        status, _, new_cookie = self.request('/api/auth/register', {'name': 'New', 'email': 'new@example.com', 'password': 'strong-password'})
        self.assertEqual(status, 200)
        self.assertNotIn('premium', self.request('/api/auth/status', cookie=new_cookie)[1]['account'])
        self.assertEqual(len(self.request('/api/folders', cookie=new_cookie)[1]['folders']), 1)
        self.assertEqual(self.request('/api/dashboard?folder_id=' + legacy_id, cookie=new_cookie)[0], 403)
        folder_id = self.request('/api/folders', cookie=new_cookie)[1]['folders'][0]['id']
        self.assertEqual(self.request('/api/folders/create', {'name': 'Another'}, new_cookie)[0], 403)
        self.assertEqual(self.request('/api/admin', cookie=new_cookie)[0], 403)
        self.assertEqual(self.request('/api/admin/update', {'field': 'premium', 'user_id': self.request('/api/folders', cookie=new_cookie)[1]['folders'][0]['owner_id'], 'value': True}, new_cookie)[0], 403)
        self.assertEqual(self.request('/api/cabinet?folder_id=' + folder_id, cookie=new_cookie)[1]['connections']['vk']['url'], '')
        empty = self.request('/api/dashboard?folder_id=' + folder_id, cookie=new_cookie)[1]
        self.assertEqual([p['id'] for p in empty['platforms']], ['vk', 'telegram', 'max'])
        self.assertEqual(empty['posts'], [])
        with patch.object(server, 'run_sync', return_value={'connections': []}):
            self.assertEqual(self.request('/api/connections/save', {'folder_id': folder_id, 'platform': 'vk', 'url': 'https://vk.ru/new'}, new_cookie)[0], 200)
        self.assertEqual(server.load_connections(legacy_id)['vk']['url'], 'https://vk.ru/old')
        rename = {'folder_id': folder_id, 'name': '  Новый проект  '}
        self.assertEqual(self.request('/api/folders/rename', rename, owner_cookie)[0], 403)
        self.assertEqual(self.request('/api/folders/rename', {'folder_id': folder_id, 'name': '   '}, new_cookie)[0], 400)
        status, result, _ = self.request('/api/folders/rename', rename, new_cookie)
        self.assertEqual(status, 200)
        self.assertEqual(result['folder']['name'], 'Новый проект')
        self.assertEqual(self.request('/api/folders', cookie=new_cookie)[1]['folders'][0]['name'], 'Новый проект')
        self.assertEqual(server.load_connections(folder_id)['vk']['url'], 'https://vk.ru/new')
        user_id = self.request('/api/folders', cookie=new_cookie)[1]['folders'][0]['owner_id']
        self.assertEqual(self.request('/api/admin/update', {'field': 'project_blocked', 'user_id': user_id, 'folder_id': folder_id, 'platform': 'vk', 'value': True}, owner_cookie)[0], 200)
        self.assertEqual(self.request('/api/connections/save', {'folder_id': folder_id, 'platform': 'vk', 'url': 'https://vk.ru/new'}, new_cookie)[0], 403)
        self.assertNotIn('vk', self.request('/api/cabinet?folder_id=' + folder_id, cookie=new_cookie)[1]['connections'])
        self.assertEqual([p['id'] for p in self.request('/api/dashboard?folder_id=' + folder_id, cookie=new_cookie)[1]['platforms']], ['telegram', 'max'])
        self.assertEqual(self.request('/api/admin/update', {'field': 'project_blocked', 'user_id': user_id, 'folder_id': folder_id, 'platform': 'vk', 'value': False}, owner_cookie)[0], 200)
        self.assertEqual(self.request('/api/admin/update', {'field': 'premium', 'user_id': user_id, 'value': True}, owner_cookie)[0], 200)
        self.assertTrue(self.request('/api/auth/status', cookie=new_cookie)[1]['account']['premium'])
        self.assertEqual(self.request('/api/folders/create', {'name': 'Second'}, new_cookie)[0], 200)
        self.assertEqual(self.request('/api/folders/create', {'name': 'Third'}, new_cookie)[0], 200)
        self.assertEqual(self.request('/api/folders/create', {'name': 'Fourth'}, new_cookie)[0], 403)
        self.assertEqual(self.request('/api/admin/update', {'field': 'premium', 'user_id': user_id, 'value': False}, owner_cookie)[0], 200)
        self.assertEqual(self.request('/api/folders/create', {'name': 'Fourth'}, new_cookie)[0], 403)
        self.assertEqual(self.request('/api/admin/update', {'field': 'folder_blocked', 'user_id': user_id, 'folder_id': folder_id, 'value': True}, owner_cookie)[0], 200)
        self.assertEqual(self.request('/api/dashboard?folder_id=' + folder_id, cookie=new_cookie)[0], 403)
        self.assertEqual(self.request('/api/folders/rename', rename, new_cookie)[0], 403)
        self.assertEqual(self.request('/api/admin/update', {'field': 'blocked', 'user_id': user_id, 'value': True}, owner_cookie)[0], 200)
        self.assertEqual(self.request('/api/folders', cookie=new_cookie)[0], 401)

    def test_history_months_quarters_and_vk_archive(self):
        _, _, cookie = self.request('/api/auth/login', {'email': 'necit0186@gmail.com', 'password': 'old-password'})
        folder_id = self.request('/api/folders', cookie=cookie)[1]['folders'][0]['id']
        configs = server.load_connections(folder_id)
        configs['vk'].update({'token': 'fake-token', 'target_id': '123'})
        configs['telegram']['url'] = 'https://t.me/example'
        server.write_secure_json(server.folder_path(folder_id, 'connections.json'), configs)
        post = {'id': 'telegram-42', 'platform': 'telegram', 'published_at': '2025-01-12T09:00:00+00:00', 'reach': 70, 'reactions': 7}
        server.write_runtime(folder_id, {
            'platforms': {'telegram': {'recent_posts': [post]}},
            'snapshots': [
                {'platform': 'telegram', 'captured_at': '2025-01-01T10:00:00+00:00', 'subscribers': 100},
                {'platform': 'telegram', 'captured_at': '2025-01-30T10:00:00+00:00', 'subscribers': 120},
                {'platform': 'telegram', 'captured_at': '2025-02-01T10:00:00+00:00', 'subscribers': 121},
                {'platform': 'telegram', 'captured_at': '2025-02-28T10:00:00+00:00', 'subscribers': 130},
            ],
            'daily_snapshots': {'2025-01-30': {'telegram': {'platform': 'telegram', 'captured_at': '2025-01-30T18:00:00+00:00', 'subscribers': 125}}},
            'post_archive': {'telegram:telegram-42': post},
        })
        base = '/api/history/report?folder_id=' + folder_id + '&year=2025&grouping='
        status, data, _ = self.request(base + 'month', cookie=cookie)
        self.assertEqual(status, 200)
        january = next(row for row in data['rows'] if row['period'] == 1 and row['platform'] == 'telegram')
        self.assertEqual((january['audience'], january['audience_change'], january['posts'], january['post_views']), (125, 25, 1, 70))
        self.assertIsNone(next(row for row in data['rows'] if row['period'] == 3 and row['platform'] == 'telegram')['audience'])
        quarter = self.request(base + 'quarter', cookie=cookie)[1]
        first = next(row for row in quarter['rows'] if row['period'] == 1 and row['platform'] == 'telegram')
        self.assertEqual((first['audience'], first['audience_change'], first['posts']), (130, 30, 1))
        self.assertEqual(self.request('/api/history/report?folder_id=' + folder_id + '&year=2100', cookie=cookie)[0], 400)
        point = int(datetime(2025, 1, 1, tzinfo=timezone.utc).timestamp())
        with patch.object(server, 'fetch_json', return_value={'response': [{'period_from': point, 'reach': {'reach': 900}}]}) as fetch:
            status, _, _ = self.request('/api/history/backfill', {'folder_id': folder_id, 'year': 2025}, cookie)
        self.assertEqual(status, 200)
        self.assertIn('interval=month', fetch.call_args.args[0])
        month = self.request(base + 'month', cookie=cookie)[1]
        vk = next(row for row in month['rows'] if row['period'] == 1 and row['platform'] == 'vk')
        self.assertEqual(vk['vk_reach'], 900)
        self.assertIsNone(vk['audience'])
        self.assertIsNone(vk['post_views'])
        with patch.object(server, 'fetch_json', return_value={'error': {'error_msg': 'Нет доступа'}}):
            self.assertEqual(self.request('/api/history/backfill', {'folder_id': folder_id, 'year': 2024}, cookie)[0], 400)
        user_id = self.request('/api/folders', cookie=cookie)[1]['folders'][0]['owner_id']
        self.assertEqual(self.request('/api/admin/update', {'field': 'project_blocked', 'user_id': user_id, 'folder_id': folder_id, 'platform': 'vk', 'value': True}, cookie)[0], 200)
        blocked = self.request(base + 'month', cookie=cookie)[1]
        self.assertNotIn('vk', blocked['platforms'])
        self.assertEqual(self.request('/api/history/backfill', {'folder_id': folder_id, 'year': 2025}, cookie)[0], 403)

    def test_daily_history_is_saved_during_sync(self):
        folder_id = next(iter(server.read_secure_json(server.FOLDERS_FILE, {})))
        with patch.object(server, 'sync_vk', return_value={'configured': True, 'status': 'connected', 'url': 'https://vk.ru/old', 'subscribers': 250, 'recent_posts': []}):
            server.run_sync(folder_id)
        runtime = server.read_runtime(folder_id)
        today = datetime.now(timezone.utc).date().isoformat()
        self.assertEqual(runtime['daily_snapshots'][today]['vk']['subscribers'], 250)
        self.assertIn('post_archive', runtime)


if __name__ == '__main__':
    unittest.main()
