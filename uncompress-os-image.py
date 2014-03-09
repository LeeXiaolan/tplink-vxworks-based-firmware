#!/usr/bin/env python2
'''
Decompress os-image partitions from TP-LINK VxWorks-based router firmware.
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
import zlib

try:
  import binwalk
except ImportError:
  binwalk = None

def getOffset(fn):
  '''
  Find the first valid zlib header.
  '''
  for result in binwalk.Modules().execute(fn, '-q', signature=True)[0].results:
    if result.description.lower().startswith('zlib') and result.valid:
      return result.offset
  return -1

def extract(fn, data):
  idx = getOffset(fn)
  if idx == -1:
    raise Exception('Can not find zlib compressed data.')
  do = zlib.decompressobj()
  uncompData = do.decompress(data[idx:])
  if do.unused_data:
    print 'Unused trailing data length: %d.' % len(do.unused_data)
  print 'Uncompress data length: %d.' % len(uncompData)
  decFileName = fn + '.uncompressed'
  with open(decFileName, 'wb') as f:
    f.write(uncompData)
  print 'Uncompressed content saved to "%s".' % decFileName

def main(fn):
  with open(fn, 'rb') as f:
    data = f.read()
  extract(fn, data)

if __name__ == '__main__':
  if binwalk is None:
    print >>sys.stderr, 'Install binwalk(http://binwalk.org) first.'
    sys.exit(1)
  if len(sys.argv) != 2:
    print >>sys.stderr, """Usage: %s OS-IMAGE\n"""%sys.argv[0]
    sys.exit(1)
  sys.exit(main(sys.argv[1]))

# vim: fenc=utf8 sw=2 ts=2
