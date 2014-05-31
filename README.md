TP-LINK VxWorks-based router firmware utilities
===============================================

Tools for working with TP-LINK VxWorks-based router firmware.

fw
--
```
fw unpack [-v... -r DIR] FILE
fw pack [-v... -r DIR -m MODEL] FILE
fw check-md5 [-v... -m MODEL] FILE
fw fix-md5 [-v... -m MODEL] FILE
```

* `unpack`    Extract partition data from firmware update file.
* `pack`      Repack up and generate firmware update file.
* `check-md5` Check firmware's MD5.
* `fix-md5`   Fix firmware's MD5.

decompress-web-res.py
---------------------
```
decompress-web-res.py FILE
```
Decompress `web-res` which extracted by `fw unpack ...`.

unow2fs.py
----------
```
unow2fs.py FILE OUT_DIR
```
Extract files in `FILE`(`web-res.decompressed`, decompressed by `decompress-web-res.py`) into `OUT_DIR`.

uncompress-os-image.py
----------------------
```
uncompress-os-image.py OS-IMAGE
```
Locate and decompress zlib stream in `os-image` which extracted by `fw unpack ...`.
