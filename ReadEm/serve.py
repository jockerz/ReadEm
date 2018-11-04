#!/usr/bin/python3
import argparse
import codecs
import html
import io
import mimetypes
import os
import posixpath
import time
import shutil
import sys
import urllib.parse
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, HTTPServer
from markdown import markdown

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
	<title>{markdown_title}</title>
	<style>{style}</style>
</head>
<body>
	<div id="mySidenav" class="sidenav">
		<a href="javascript:void(0)" class="closebtn" onclick="closeNav()">&times;</a>
		{menu}
		<a class="repo-link" href="https://github.com/jockerz/ReadEm">About</a>
	</div>
	<span class="navbar" style="font-size:30px;cursor:pointer" onclick="openNav()">
		<div class="main" style="padding: 10px;">
			&#9776; Menu
		</div>
	</span>
	<div class="main">
		<div class="markdown-body" id="content">
			{markdown_content}
		</div>
	</div>
	{javascript}
</body>
</html>
"""


class CostumRequestHandler(SimpleHTTPRequestHandler):
	"""
	SimpleHTTPRequestHandler alike for markdown file
	features:
	- add markdown_to_html method
	- make special do_GET function treat .md file well
	"""
	asset_path = os.path.join(os.path.dirname(__file__), 'assets')
	base_path = os.getcwd()

	def get_asset(self, filename):
		data = ""
		try:
			f = open(os.path.join(self.asset_path, filename), 'r', encoding='utf-8')
			data = f.read()
			f.close()
			return data
		except Exception as e:
			raise e
			return ""

	def markdown_to_html(self, path):
		"""
		Read markdown file, load it to HTML_TEMPLATE
		return file descriptor that contain html string 
		"""
		md = codecs.open(path, mode="r", encoding="utf-8")
		data = md.read()
		md.close()
		
		js_data = "<script>"
		js_data += self.get_asset('app.js') + "</script>"
		
		css_data = self.get_asset('github.css')
		css_data += self.get_asset('app.css')
		
		enc = sys.getfilesystemencoding()

		title_path = self.path.strip()
		if title_path[0] == "/":
			title_path = title_path[1:]
			title_path, _ = posixpath.splitext(title_path)
			title_path = urllib.parse.unquote(title_path)

		data = HTML_TEMPLATE.format(
			markdown_title = title_path,
			markdown_content = markdown(data, extensions=[
				'attr_list',	# {: #someid .someclass somekey='some value' }
				'fenced_code', 	# github style syntax highlighting
				'smarty',
				'tables',
			]),
			javascript = js_data,
			menu = self.get_menu(),
			style = css_data)

		encoded = data.encode(enc, 'surrogateescape')

		f = io.BytesIO()
		f.write(encoded)
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
		li_template = "<a href=\"{}\">{}</a>"
		path = self.translate_path(self.path)
		menu = []

		try:
			contents = os.listdir(os.path.dirname(path))
			if os.path.dirname(path) != self.base_path:
				contents.append("..")
		except OSError as e:
			return ""
		contents.sort(key=lambda a: a.lower())

		enc = sys.getfilesystemencoding()
		
		for c in contents:
			fullname = os.path.join(os.path.dirname(self.path), c)
			displayname = c
			is_good = False
			
			if os.path.isdir(c):
				displayname = c + "/"
				is_good = True
			
			if os.path.islink(c):
				displayname = c + "@"
				is_good = True
			
			_, ext = posixpath.splitext(fullname)
			if "md" in ext or "markdown" in ext:
				displayname = c.replace(ext, "")
				is_good = True

			if not is_good:
				continue
			
			c = os.path.join(os.path.dirname(self.path), c)

			menu.append(li_template.format(
				urllib.parse.quote(c, errors='surrogatepass'), 
				html.escape(displayname)))
		
		return "\n".join(menu)

	def do_GET(self):
		"""
		Serve a GET request.
		if file requested is markdown file,
		load it using markdown_to_html method
		"""
		path = self.translate_path(self.path)
		if os.path.isdir(path):
			readme_file1 = os.path.join(path, "README.md")
			readme_file2 = os.path.join(path, "readme.md")
			readme_file3 = os.path.join(path, "README.markdown")
			readme_file4 = os.path.join(path, "readme.markdown")
			if os.path.exists(readme_file1):
				self.path = os.path.relpath(readme_file1)
			elif os.path.exists(readme_file2):
				self.path = os.path.relpath(readme_file2)
			elif os.path.exists(readme_file3):
				self.path = os.path.relpath(readme_file3)
			elif os.path.exists(readme_file3):
				self.path = os.path.relpath(readme_file3)
		path = self.translate_path(self.path)

		if (self.path.endswith("md") or \
			self.path.endswith("markdown")) and \
			os.path.exists(path):
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
	parser.add_argument('--bind', '-b', default='127.0.0.1', metavar='ADDRESS',
		help='Specify alternate bind address '
			 '[default: 127.0.0.1]')
	parser.add_argument('port', action='store',
		default=8000, type=int,
		nargs='?',
		help='Specify alternate port [default: 8000]')
	args = parser.parse_args()

	httpd = HTTPServer((args.bind, args.port), CostumRequestHandler)
	try:
		print("Listening on {}:{}".format(args.bind, args.port))
		print("Press CTRL + c to stop")
		httpd.serve_forever()
	except KeyboardInterrupt:
		print("Stopped")
	except Exception as e:
		print("Exception: {}".format(e))
