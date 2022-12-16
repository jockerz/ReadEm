#!/usr/bin/python3
import argparse
import codecs
import html
import io
import os
import pathlib
import posixpath
import shutil
import sys
import urllib.parse
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, HTTPServer
from markdown import markdown

IGNORED_ITEMS = ['.git', 'README.md']
MD_FILES = [
    "README.md", "readme.md", "README.markdown",
    "readme.markdown"
]

# ReadEm source directory
BASEDIR = os.path.dirname(__file__)


class MDRequestHandler(SimpleHTTPRequestHandler):
    init_path = BASEDIR
    asset_path = os.path.join(BASEDIR, 'assets')
    tpl_path = os.path.join(BASEDIR, 'templates')
    template_name = "default.html"
    md_base_path = pathlib.Path.cwd()

    def get_asset(self, filename):
        with open(
            os.path.join(self.asset_path, filename), 'r', encoding='utf-8'
        ) as f:
            data = f.read()
        return data

    def markdown_to_html(self, path):
        """
        Read markdown file, load it to HTML_TEMPLATE
        return file descriptor that contain html string 
        """
        md = codecs.open(path, mode="r", encoding="utf-8")
        data = md.read()
        md.close()
        
        js_data = "<script>" + self.get_asset('app.js') + "</script>"
        css_data = self.get_asset('github.css') + self.get_asset('app.css')
        
        enc = sys.getfilesystemencoding()

        title_path = self.path.strip()
        if title_path[0] == "/":
            title_path = title_path[1:]
            title_path, _ = posixpath.splitext(title_path)
            title_path = urllib.parse.unquote(title_path)

        with open(os.path.join(self.tpl_path, self.template_name)) as fd:
            data = fd.read().format(
                markdown_title=title_path,
                markdown_content=markdown(data, extensions=[
                    'attr_list',    # {: #someid .someclass somekey='some value' }
                    'fenced_code',  # github style syntax highlighting
                    'smarty',
                    'tables',
                ]),
                javascript=js_data,
                menu=self.get_menu(),
                style=css_data
            )

        f = io.BytesIO()
        f.write(data.encode(enc, 'surrogateescape'))
        f.seek(0)

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()

        return f

    def get_menu(self):
        """
        return html string of content list on directory,
        """
        path = self.translate_path(self.path)
        menu = []

        try:
            contents = os.listdir(os.path.dirname(path))
            if os.path.dirname(path) != str(self.md_base_path):
                # fullname = os.path.join(os.path.dirname(self.path), content)
                fullname = os.path.join(os.path.dirname(self.path), "..")
                href = urllib.parse.quote(fullname, errors='surrogatepass')
                menu.append(f"<a href=\"{href}\">Home</a>")

            menu.append("<hr/>")
        except OSError:
            return ""
        contents.sort(key=lambda a: a.lower())
        
        for content in contents:
            if content in IGNORED_ITEMS:
                continue

            if os.path.isdir(content):
                display_name = content + "/"
            elif os.path.islink(content):
                display_name = content + "@"
            else:
                display_name = content

            fullname = os.path.join(os.path.dirname(self.path), content)
            fullpath = os.path.join(
                self.md_base_path, fullname.replace(os.path.sep, "", 1)
            )
            _, ext = posixpath.splitext(fullname.lower())
            if "md" in ext or "markdown" in ext:
                display_name = content.replace(ext, "")
            elif os.path.isfile(fullpath):
                continue

            menu.append(
                f"<a href=\"{urllib.parse.quote(fullname, errors='surrogatepass')}\">"
                f"{html.escape(display_name)}</a>"
            )
        
        return "\n".join(menu)

    def do_GET(self):
        """
        Serve a GET request.
        if file requested is markdown file,
        load it using markdown_to_html method
        """
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            for file in MD_FILES:
                file_path = os.path.join(path, file)
                if os.path.exists(file_path):
                    self.path = os.path.relpath(file_path)
        path = self.translate_path(self.path)

        if (self.path.endswith(".md") or self.path.endswith(".markdown")) \
                and os.path.exists(path):
            md = self.markdown_to_html(path)
            try:
                shutil.copyfileobj(md, self.wfile)
            finally:
                md.close()
            return

        f = self.send_head()
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--bind', '-b', default='127.0.0.1', metavar='ADDRESS',
        help='Specify alternate bind address '
             '[default: 127.0.0.1]'
    )
    parser.add_argument(
        'port', action='store', default=8000, type=int,
        nargs='?', help='Specify alternate port [default: 8000]'
    )
    args = parser.parse_args()

    http = HTTPServer((args.bind, args.port), MDRequestHandler)
    try:
        print("Listening on http://{}:{}".format(args.bind, args.port))
        print("Press CTRL + c to stop")
        http.serve_forever()
    except KeyboardInterrupt:
        print("Stopped")
    except Exception as e:
        print("Exception: {}".format(e))
