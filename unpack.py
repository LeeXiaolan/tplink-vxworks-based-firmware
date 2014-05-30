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

import os
import os.path
import sys

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print >>sys.stderr, """Usage: %s FILE\n"""%sys.argv[0]
    sys.exit(1)
  fw = os.path.join(os.path.dirname(__file__), 'fw')
  os.system('%s unpack "%s"' % (fw, sys.argv[1]))

# vim: fenc=utf8 sw=2 ts=2
