#!/usr/bin/env python2
'''
Extract partitions from TP-LINK VxWorks-based router firmware.
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

import re
import sys

def parsePt(mv):
  for i in xrange(min(len(mv), 1024)):
    if mv[i] == '\x00':
      end = i
      break
  else:
    raise ValueError('Not \\x00 terminated.')
  arr = re.split(r'\t\r\n', mv[:end].tobytes())

  result = list()
  for i in arr:
    if len(i) > 0:
      items = i.split()
      if len(items) > 0 and (len(items) % 2 == 0):
        d = dict()
        for j in xrange(0, len(items), 2):
          key, value = items[j], items[j + 1]
          if key == 'base' or key == 'size':
            d[key] = int(value, 16)
          else:
            d[key] = value
        result.append(d)
  return result

def extract(mv, pt):
  for item in pt:
    with open(item['fwup-ptn'], 'wb') as of:
      base, size = item['base'], item['size']
      of.write(mv[base:base + size].tobytes())

def main(fn):
  with open(fn, 'rb') as f:
    data = f.read()
    mv = memoryview(data)[0x5c:]
    pt = parsePt(mv)
    extract(mv, pt)

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print >>sys.stderr, """Usage: %s FILE\n"""%sys.argv[0]
    sys.exit(1)
  main(sys.argv[1])

# vim: fenc=utf8 sw=2 ts=2
