#!/usr/bin/env python2
'''
Unpack TP-LINK VxWorks-based routers' compiled web resouce files.
Copyright (C) 2014 Xiaolan.Lee<LeeXiaolan@gmail.com>
License: GPLv2 (see LICENSE for details).

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
'''

import sys
import struct

try: import lzma
except ImportError:
  try: from backports import lzma
  except ImportError:
    lzma = None

def main(fn):
  with open(fn, 'rb') as f:
    data = f.read()
    compressedLength = struct.unpack('>I', data[0:4])[0]
    if compressedLength + 9 != len(data):
      raise Exception('Unknown file format.')

  decompressor = lzma.LZMADecompressor(format=lzma.FORMAT_ALONE)
  decompressedData = decompressor.decompress(data[9:])
  print "Decompressed data length: %d" % len(decompressedData)
  if decompressor.unused_data:
  	print "Unused data length: %d" % len(decompressor.unused_data)
  decompressedFileName = fn + '.decompressed'
  with open(decompressedFileName, 'wb') as f:
    f.write(decompressedData)
  print 'Decompressed data saved to "%s".' % decompressedFileName
  sys.exit(0)

if __name__ == '__main__':
  if lzma is None:
    print >>sys.stderr, "Install lzma package first."
    sys.exit(2)
  if len(sys.argv) != 2:
    print >>sys.stderr, """Usage: %s FILE\n"""%sys.argv[0]
    sys.exit(1)
  main(sys.argv[1])

# vim: fenc=utf8 sw=2 ts=2
