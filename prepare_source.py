"""Prepare a review-only G973N kernel build; never writes a device partition."""
from pathlib import Path
import hashlib
import lzma
import sys
import urllib.request
import zipfile

root = Path(sys.argv[1]).resolve()
apk = Path(sys.argv[2]).resolve()
expected = '89cefac0a318afa39fb3880c45c87b036c05bc1ebf02a7a715b7f8d7c26ac6e7'
if not apk.exists():
    urllib.request.urlretrieve('https://github.com/topjohnwu/Magisk/releases/download/v31.1/Magisk-v31.1.apk', apk)
if hashlib.sha256(apk.read_bytes()).hexdigest() != expected:
    raise SystemExit('Magisk APK checksum mismatch')
config = root / 'arch/arm64/configs/exynos9820-beyond1lteks_defconfig'
if not config.is_file():
    raise SystemExit('Missing Korean G973N config; do not substitute G973F')
builder = root / 'cruelbuild'
text = builder.read_text()
needle = "models = {\n"
if text.count(needle) != 1:
    raise SystemExit('Unexpected upstream build script')
text = text.replace(needle, needle + "    'G973N': {'config': 'exynos9820-beyond1lteks_defconfig'},\n", 1)
builder.write_text(text)
dest = root / 'usr/magisk'
with zipfile.ZipFile(apk) as z:
    (dest / 'magiskinit').write_bytes(z.read('lib/arm64-v8a/libmagiskinit.so'))
    for source, target in [('libmagisk.so', 'magisk.xz'), ('libinit-ld.so', 'init-ld.xz')]:
        raw = z.read('lib/arm64-v8a/' + source)
        (dest / target).write_bytes(lzma.compress(raw, format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC32))
(dest / 'magisk_version').write_text('v31.1')
(dest / 'update_magisk.sh').write_text('''#!/bin/bash
set -eu
cd "$(dirname "$0")"
test "${1:-v31.1}" = v31.1
test -s magiskinit && test -s magisk.xz && test -s init-ld.xz
echo 'Using checksum-verified Magisk v31.1 payload'
''')
(dest / 'update_magisk.sh').chmod(0o755)
(dest / 'initramfs_list').write_text('''dir /.backup 0700 0 0
file /init usr/magisk/magiskinit 0750 0 0
file /.backup/.magisk usr/magisk/backup_magisk 0600 0 0
dir /overlay.d 0750 0 0
dir /overlay.d/sbin 0750 0 0
file /overlay.d/sbin/magisk.xz usr/magisk/magisk.xz 0644 0 0
file /overlay.d/sbin/init-ld.xz usr/magisk/init-ld.xz 0644 0 0
''')
print('Prepared G973N config and Magisk 31.1 payload. Boot compatibility remains untested.')
