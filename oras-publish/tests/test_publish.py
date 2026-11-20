# SPDX-FileCopyrightText: 2026 Greenbone AG
# SPDX-License-Identifier: GPL-3.0-or-later
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'publish.sh'
DIGEST = 'sha256:' + 'a' * 64


class PublishTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.file = self.root / 'packages' / '--firmware:with spaces.cos'
        self.file.parent.mkdir()
        self.file.write_bytes(b'firmware')
        fake = self.root / 'oras'
        fake.write_text('''#!/usr/bin/env python3
import json, os, pathlib, sys
args = sys.argv[1:]
entry = dict(tool=pathlib.Path(sys.argv[0]).name, args=args,
             config=os.environ['DOCKER_CONFIG'], cwd=os.getcwd())
if args[0] == 'login':
    entry['password'] = sys.stdin.read()
    pathlib.Path(entry['config'], 'config.json').write_text('{}')
with open(os.environ['LOG'], 'a') as log:
    log.write(json.dumps(entry) + '\\n')
if args[0] == os.environ.get('FAIL_COMMAND'):
    sys.exit(23)
if args[:2] == ['manifest', 'fetch']:
    if os.environ.get('LOOKUP_ERROR'):
        print(os.environ['LOOKUP_ERROR'], file=sys.stderr)
        sys.exit(17)
    print(json.dumps({'digest': os.environ['RESULT_DIGEST']}))
if args[0] == 'push':
    print(json.dumps({'digest': os.environ['RESULT_DIGEST']}))
''')
        fake.chmod(0o755)
        (self.root / 'cosign').symlink_to(fake)
        self.env = dict(os.environ, PATH=f'{self.root}:{os.environ["PATH"]}',
                        ARTIFACT_FILE=str(self.file), ARTIFACT_URL='registry.example:5000/team/cos:v1',
                        ARTIFACT_TYPE='', MEDIA_TYPE='application/octet-stream',
                        ANNOTATIONS='', ANNOTATION_FILE='', EXPORT_MANIFEST='',
                        REGISTRY_USER='user', REGISTRY_TOKEN='secret', SIGN='false', PREVENT_OVERWRITE='false',
                        COSIGN_KEY='', COSIGN_PASSWORD='', COSIGN_TLOG_UPLOAD='true',
                        RUNNER_TEMP=str(self.root), GITHUB_OUTPUT=str(self.root / 'output'),
                        LOG=str(self.root / 'log'), RESULT_DIGEST=DIGEST)

    def run_publish(self, **changes):
        return subprocess.run(['bash', str(SCRIPT)], cwd=self.root,
                              env=dict(self.env, **changes), capture_output=True, text=True)

    def calls(self):
        return [json.loads(line) for line in (self.root / 'log').read_text().splitlines()]

    def assert_cleaned(self):
        self.assertEqual(list(self.root.glob('oras-publish.*')), [])

    def test_metadata_paths_and_output(self):
        (self.root / 'annotations.json').write_text('{}')
        result = self.run_publish(ARTIFACT_TYPE='application/vnd.greenbone.firmware.v1+tar',
                                  MEDIA_TYPE='application/vnd.greenbone.firmware.v1+tar',
                                  ANNOTATIONS='description=spaces; $(touch INJECTED)\n\nx=a=b\r\n',
                                  ANNOTATION_FILE='annotations.json', EXPORT_MANIFEST='manifest.json')
        self.assertEqual(result.returncode, 0, result.stderr)
        login, push = self.calls()
        self.assertEqual(login['password'], 'secret')
        self.assertNotIn('secret', str(push))
        args = push['args']
        self.assertIn('description=spaces; $(touch INJECTED)', args)
        self.assertIn('x=a=b', args)
        self.assertIn(str(self.root / 'annotations.json'), args)
        self.assertIn(str(self.root / 'manifest.json'), args)
        self.assertEqual(args[-1], self.file.name + ':application/vnd.greenbone.firmware.v1+tar')
        self.assertEqual(push['cwd'], str(self.file.parent))
        self.assertFalse((self.file.parent / 'INJECTED').exists())
        self.assertIn(f'reference=registry.example:5000/team/cos@{DIGEST}',
                      (self.root / 'output').read_text())
        self.assert_cleaned()

    def test_prevent_overwrite_rejects_existing_tag(self):
        result = self.run_publish(PREVENT_OVERWRITE='true', SIGN='true')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('refusing to overwrite', result.stderr)
        self.assertEqual([call['args'][0] for call in self.calls()], ['login', 'manifest'])
        lookup = self.calls()[-1]
        self.assertEqual(lookup['args'][-1], self.env['ARTIFACT_URL'])
        self.assertIn(str(Path(lookup['config']) / 'config.json'), lookup['args'])
        self.assertFalse((self.root / 'output').exists())
        self.assert_cleaned()

    def test_prevent_overwrite_allows_missing_tag(self):
        for error in (f"Error: {self.env['ARTIFACT_URL']}: not found",
                      'Error: registry: MANIFEST_UNKNOWN: manifest unknown',
                      'Error: registry: NAME_UNKNOWN: repository name not known'):
            with self.subTest(error=error):
                result = self.run_publish(PREVENT_OVERWRITE='true', LOOKUP_ERROR=error)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual([call['args'][0] for call in self.calls()[-3:]],
                                 ['login', 'manifest', 'push'])
                self.assertIn(DIGEST, (self.root / 'output').read_text())
                self.assert_cleaned()

    def test_lookup_errors_prevent_upload(self):
        for error in ('unauthorized', 'TLS handshake failed', 'connection refused',
                      'Error: credentials: not found', 'response status code 500',
                      'unrecognized response', 'Error: executable file not found'):
            with self.subTest(error=error):
                result = self.run_publish(PREVENT_OVERWRITE='true', LOOKUP_ERROR=error, SIGN='true')
                self.assertEqual(result.returncode, 17)
                self.assertEqual([call['args'][0] for call in self.calls()[-2:]], ['login', 'manifest'])
                self.assertFalse((self.root / 'output').exists())
                self.assert_cleaned()

    def test_signing_uses_digest_and_key(self):
        result = self.run_publish(SIGN='true', COSIGN_KEY='private-key', COSIGN_TLOG_UPLOAD='false')
        self.assertEqual(result.returncode, 0, result.stderr)
        sign = self.calls()[-1]
        self.assertEqual(sign['tool'], 'cosign')
        self.assertIn('env://COSIGN_KEY', sign['args'])
        self.assertIn('--tlog-upload=false', sign['args'])
        self.assertEqual(sign['args'][-1], f'registry.example:5000/team/cos@{DIGEST}')
        self.assert_cleaned()

    def test_keyless_signing(self):
        result = self.run_publish(SIGN='true')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('--key', self.calls()[-1]['args'])

    def test_failures_propagate_and_cleanup(self):
        for command in ('login', 'push', 'sign'):
            with self.subTest(command=command):
                result = self.run_publish(SIGN='true', FAIL_COMMAND=command)
                self.assertEqual(result.returncode, 23, result.stderr)
                self.assertFalse((self.root / 'output').exists())
                self.assert_cleaned()

    def test_invalid_input_does_not_login(self):
        for changes in ({'ANNOTATIONS': 'missing-equals'}, {'REGISTRY_TOKEN': ''},
                        {'ARTIFACT_URL': 'https://registry.example/repo:v1'},
                        {'ARTIFACT_URL': 'registry.example/repo'}, {'SIGN': 'yes'},
                        {'ARTIFACT_FILE': 'missing.cos'}, {'PREVENT_OVERWRITE': 'yes'}):
            with self.subTest(changes=changes):
                self.assertNotEqual(self.run_publish(**changes).returncode, 0)
                self.assertFalse((self.root / 'log').exists())

    def test_invalid_digest_is_not_reported_or_signed(self):
        result = self.run_publish(SIGN='true', RESULT_DIGEST='invalid')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(len(self.calls()), 2)
        self.assertFalse((self.root / 'output').exists())
        self.assert_cleaned()


if __name__ == '__main__':
    unittest.main()
