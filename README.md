## ReadEm

> HTTP server for readme files.

Read local README.md or any markdown file easily.
Will be useful for clone wiki of github repository or the repo clone with markdown files.
Basicly any `.md` (markdown) file.

Markdown files on current directory will be shown on navbar menu. :)


## Instalation

```bash
$ pip3 install ReadEm
```

## Run

```bash
ON_A_DIRECTORY: $ python3 -m ReadEm.read_em -h
usage: read_em.py [-h] [--bind ADDRESS] [port]

positional arguments:
  port                  Specify alternate port [default: 8000]

optional arguments:
  -h, --help            show this help message and exit
  --bind ADDRESS, -b ADDRESS
                        Specify alternate bind address [default: 127.0.0.1]

ON_A_DIRECTORY: $ python3 -m ReadEm.read_em
Listening on 127.0.0.1:8000
Press CTRL+c to stop
127.0.0.1 - - [22/Dec/2017 14:24:40] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [22/Dec/2017 14:45:17] "GET /README.md HTTP/1.1" 200 
```


## Credit

- [GitHub Markdown CSS](https://github.com/sindresorhus/github-markdown-css)
- [Python Markdown](https://python-markdown.github.io/)

