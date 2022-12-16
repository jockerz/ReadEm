## ReadEm: HTTP server for markdown files

Useful for:

- Previewing markdown files at ease, for your repository or anything.
- Markdown files on current directory is shown on navbar.


## Installation

```bash
$ pip3 install ReadEm
```

## Run

```bash
$ python3 -m ReadEm.serve -h
usage: serve.py [-h] [--bind ADDRESS] [port]

positional arguments:
  port                  Specify alternate port [default: 8000]

optional arguments:
  -h, --help            show this help message and exit
  --bind ADDRESS, -b ADDRESS
                        Specify alternate bind address [default: 127.0.0.1]

$ python3 -m ReadEm.serve
Listening on http://127.0.0.1:8000
Press CTRL+c to stop
127.0.0.1 - - [22/Dec/2017 14:24:40] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [22/Dec/2017 14:45:17] "GET /README.md HTTP/1.1" 200 -
127.0.0.1 - - [08/Jun/2018 01:40:21] "GET /README.md HTTP/1.1" 200 -
```

Then open [127.0.0.1:8000](http://127.0.0.1:8000) on your browser.

## Credit

- [GitHub Markdown CSS](https://github.com/sindresorhus/github-markdown-css)
- [Python Markdown](https://python-markdown.github.io/)
