CommonMark-py
=============

Pure Python port of [jgm](https://github.com/jgm)'s [stmd.js](https://github.com/jgm/stmd/blob/master/js/stmd.js), a Markdown parser and renderer for the [CommonMark](http://commonmark.org) specification, using only native modules. Once both this project and the CommonMark specification are stable we will release the first `1.0` version and attempt to keep up to date with changes in `stmd.js`.

We are currently at the same development stage (actually a bit ahead because we have implemented HTML entity conversion and href URL escaping) as `stmd.js`. Since Python versions pre-3.4 use outdated (i.e. not HTML5 spec) entity conversion, I've converted the 3.4 implementation into a single file, `entitytrans.py` which so far seems to work (all tests pass on 2.7, 3.3, 3.4, PyPy, and PyPy3).

**Current version:** 0.5.4

[![Build Status](https://travis-ci.org/rolandshoemaker/CommonMark-py.svg?branch=master)](https://travis-ci.org/rolandshoemaker/CommonMark-py)

Installation
------------

    rolands@kamaji:~$ pip install commonmark

Usage
-----

	import CommonMark
	parser = CommonMark.DocParser()
	renderer = CommonMark.HTMLRenderer()
	ast = parser.parse("Hello *World*")
	html = renderer.render(ast)
	json = CommonMark.ASTtoJSON(ast)
	CommonMark.dumpAST(ast) # pretty print generated AST structure
	print(html) # <p>Hello <em>World</em><p/>
    
    ----- or -----
    
	rolands@kamaji:~$ cmark.py README.md -o README.html
	rolands@kamaji:~$ cmark.py README.md -o README.json -aj # output AST as JSON
	rolands@kamaji:~$ cmark.py README.md -a # pretty print generated AST structure
	rolands@kamaji:~$ cmark.py -h
	usage: cmark.py [-h] [-o [O]] [-a] [-aj] [infile]

	Process Markdown according to the CommonMark specification.

	positional arguments:
	  infile      Input Markdown file to parse, defaults to stdin

	optional arguments:
	  -h, --help  show this help message and exit
	  -o [O]      Output HTML/JSON file, defaults to stdout
	  -a          Print formatted AST
	  -aj         Output JSON AST
	 
Contributing
------------

If you would like to offer suggestions/optimizations/bugfixes through pull requests please do! Also if you find an error in the parser/renderer that isn't caught by the current test suite please open a new issue and I would also suggest you send the [stmd.js](https://github.com/jgm/stmd/blob/master/js/stmd.js) project a pull request adding your test to the existing test suite.

Tests
-----

The tests script, `CommonMark-tests.py`, is pretty much a devtool. As well as running all the tests embeded in `spec.txt` it also allows you to run specific tests using the `-t` argument, provide information about passed tests with `-p`, percentage passed by category of test with `-s`, and enter markdown interactively with `-i` (In interactive mode end a block by inputing a line with just `end`, to quit do the same but with `quit`). `-d` can be used to print call tracing.

	rolands@kamaji:~/utils/CommonMark-py$ python CommonMark-tests.py -h
	usage: CommonMark-tests.py [-h] [-t T] [-p] [-f] [-i] [-d] [-np] [-s]

	script to run the CommonMark specification tests against the CommonMark.py
	parser

	optional arguments:
	  -h, --help  show this help message and exit
	  -t T        Single test to run or comma seperated list of tests (-t 10 or -t 10,11,12,13)
	  -p          Print passed test information
	  -f          Print failed tests (during -np...)
	  -i          Interactive Markdown input mode
	  -d          Debug, trace calls
	  -np         Only print section header, tick, or cross
	  -s          Print percent of tests passed by category

Authors
-------
* [Bibek Kafle](https://github.com/kafle)
* [Roland Shoemaker](https://github.com/rolandshoemaker)
