# Helloworld plugin
# -*- coding: utf-8 -*-

import tempfile
import commands
import sys
import os

from trac.core import *
from trac.mimeview.api import IHTMLPreviewRenderer

class RPMViewerPlugin(Component):
    implements(IHTMLPreviewRenderer)

    MIME_TYPES = ('application/x-rpm')

    def get_quality_ratio(self, mimetype):
        if mimetype in self.MIME_TYPES:
            return 9
        return 0

    def render(self, context, mimetype, content, filename=None, url=None):

        suffix = filename[filename.rfind('.'):]
        infilepath = tempfile.mktemp(suffix)
        tmp = open(str(infilepath), 'wb')
        tmp.write(content.read())
        tmp.close()

        buffer = []
        buffer.append(u"<h2>パッケージ情報</h2>")
        buffer.append('<pre class="wiki">')
        buffer.append(unicode(commands.getoutput("rpm -qpi " + infilepath), "utf_8"))
        buffer.append('</pre>')
        buffer.append(u"<h2>依存パッケージ</h2>")
        buffer.append('<pre class="wiki">')
        buffer.append(unicode(commands.getoutput("rpm -qpR " + infilepath), "utf_8"))
        buffer.append('</pre>')
        buffer.append(u"<h2>ファイル一覧</h2>")
        buffer.append('<pre class="wiki">')
        buffer.append(unicode(commands.getoutput("rpm -qpl " + infilepath), "utf_8"))
        buffer.append('</pre>')
        buffer.append(u"<h2>実行スクリプト</h2>")
        buffer.append('<pre class="wiki">')
        buffer.append(unicode(commands.getoutput("rpm -qp --scripts " + infilepath), "utf_8"))
        buffer.append('</pre>')
        buffer.append("<h2>Changelog</h2>")
        buffer.append('<pre class="wiki">')
        buffer.append(unicode(commands.getoutput("rpm -qp --changelog " + infilepath), "utf_8"))
        buffer.append('</pre>')

        os.unlink(infilepath)
        return u''.join(buffer)

