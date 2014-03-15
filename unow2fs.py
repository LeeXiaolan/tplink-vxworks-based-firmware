#!/usr/bin/env python2
'''
Extract web resource files from TP-LINK VxWorks-based routers' compiled web resouce files.
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

import os
import os.path
import sys
import struct

def extract(data, out):
  offset = 40
  fileCount = struct.unpack('>II', data[32:offset])[1]
  entry = struct.Struct('>64sIII')
  # Ensure all entries will be located in the data range.
  endOfEntry = offset + fileCount * entry.size
  if len(data) < endOfEntry:
    print >>sys.stderr, "File length error."
    return 2
  print 'Extract %d files into %s...' % (fileCount, out)
  failed = 0
  for i in xrange(fileCount):
    (filePath, fileSize, fileOffset, unknown,) = entry.unpack(data[offset:offset+entry.size])

    # Strip trailing '\x00'.
    filePath = filePath[0:filePath.index('\x00')]

    msg = '%s (%d) at 0x%x...' % (filePath, fileSize, fileOffset,)
    if fileOffset > len(data) or fileOffset < endOfEntry:
      # File offset not in the right range.
      msg += 'Failed: data error.'
    else:
      fileData = data[fileOffset:fileOffset+fileSize]
      if '..' in filePath:
        # For security, if ".." in path, ignore it.
        msg += 'Failed: ".." in file path.'
        failed += 1
      else:
        if filePath.startswith('/') or filePath.startswith('\\'): filePath = '.' + filePath
        filePath = os.path.join(out, filePath)
        dirs = os.path.dirname(filePath)
        # Make sure all parent directories exists.
        if not os.path.exists(dirs):
          os.makedirs(dirs)
  
        # Save file data.
        with open(filePath, 'wb') as f:
          f.write(fileData)
        msg += 'Successful'

    print msg
    offset += entry.size

  if failed:
    print '%d files failed.' % failed

def main(fn, out):
  with open(fn, 'rb') as f:
    data = f.read()
  if os.path.exists(out):
    print >>sys.stderr, "Output directory already exists."
    return 2
  # Check signature and file header.
  if data[0:32] != 'OW' * 0x10 or len(data) < 32 + 8:
    print >>sys.stderr, "Unsupported file format: %s" % fn
    return 2
  return extract(data, out)

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print >>sys.stderr, """Usage: %s FILE OUT_DIR\n"""%sys.argv[0]
    sys.exit(1)
  sys.exit(main(sys.argv[1], sys.argv[2]))

# vim: fenc=utf8 sw=2 ts=2
