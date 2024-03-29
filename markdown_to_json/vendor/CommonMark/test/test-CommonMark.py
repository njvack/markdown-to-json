#!/usr/bin/env python
from __future__ import division

import argparse
import codecs
import pprint
import re
import sys
import time

import CommonMark


class colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"


def trace_calls(frame, event, arg):
    co = frame.f_code
    func_name = co.co_name
    if func_name == "write":
        return
    line_no = frame.f_lineno
    filename = co.co_filename
    if (
        event == "call"
        and not re.match("__", func_name)
        and re.search("CommonMark.py", filename)
        and not func_name == "dumpAST"
    ):
        print(
            "-> "
            + frame.f_back.f_code.co_name
            + " at "
            + str(frame.f_back.f_lineno)
            + " called "
            + func_name
            + " at "
            + str(line_no)
            + " in "
            + filename
        )
        return trace_calls
    return


parser = argparse.ArgumentParser(
    description="script to run the CommonMark specification tests against the CommonMark.py parser"
)
parser.add_argument("-t", help="Single test to run or comma seperated list of tests (-t 10 or -t 10,11,12,13)")
parser.add_argument("-p", action="store_true", help="Print passed test information")
parser.add_argument("-f", action="store_true", help="Print failed tests (during -np...)")
parser.add_argument("-i", action="store_true", help="Interactive Markdown input mode")
parser.add_argument("-d", action="store_true", help="Debug, trace calls")
parser.add_argument("-np", action="store_true", help="Only print section header, tick, or cross")
parser.add_argument("-s", action="store_true", help="Print percent of tests passed by category")
args = parser.parse_args()

if args.d:
    sys.settrace(trace_calls)

renderer = CommonMark.HTMLRenderer()
parser = CommonMark.DocParser()

f = codecs.open("spec.txt", encoding="utf-8")
datalist = []
for line in f:
    datalist.append(line)
data = "".join(datalist)
passed = 0
failed = 0
catStats = {}
examples = []
example_number = 0
current_section = ""
tabChar = "\u2192"
spaceChar = "\u2423"
nbspChar = "\u00A0"


def showSpaces(t):
    t = re.sub("\\t", tabChar, t)
    t = re.sub(" ", spaceChar, t)
    t = re.sub(nbspChar, spaceChar, t)
    return t


t = re.sub("\r\n", "\n", data)

tests = re.sub("^<!-- END TESTS -->(.|[\n])*", "", t, flags=re.M)
testMatch = re.findall(re.compile("^\.\n([\s\S]*?)^\.\n([\s\S]*?)^\.$|^#{1,6} *(.*)$", re.M), tests)

for match in testMatch:
    if not match[2] == "":
        current_section = match[2]
    else:
        example_number += 1
        examples.append({"markdown": match[0], "html": match[1], "section": current_section, "number": example_number})

current_section = ""

startTime = time.clock()

if args.i:
    print(
        colors.OKGREEN
        + "(To end input of Markdown block enter 'end' on it's own line, to quit enter 'quit')"
        + colors.ENDC
    )
    while True:
        s = ""
        while True:
            inp = raw_input(colors.OKBLUE + "Markdown: " + colors.ENDC)
            if not inp == "end" and not inp == "quit":
                s += inp + "\n"
            elif inp == "end":
                s = s[:-1]
                break
            elif inp == "quit":
                print(colors.HEADER + "bye!" + colors.ENDC)
                exit(0)
        ast = parser.parse(s)
        html = renderer.render(ast)
        print(colors.WARNING + "=" * 10 + "AST=====" + colors.ENDC)
        CommonMark.dumpAST(ast)
        print(colors.WARNING + "=" * 10 + "HTML====" + colors.ENDC)
        print(html)

# some tests?
if args.t:
    tests = args.t.split(",")
    choice_examples = []
    for t in tests:
        if not t == "" and len(examples) > int(t):
            choice_examples.append(examples[int(t) - 1])
    examples = choice_examples

# all tests

for i, example in enumerate(examples):  # [0,examples[0]]
    if not example["section"] == "" and not current_section == example["section"]:
        print(colors.HEADER + "[" + example["section"] + "]" + colors.ENDC)
        current_section = example["section"]
        catStats.update({current_section: [0, 0, 0]})

    catStats[current_section][2] += 1
    if args.d:
        print(colors.HEADER + "[Parsing]" + colors.ENDC)
    ast = parser.parse(re.sub(tabChar, "\t", example["markdown"]))
    if args.d:
        print(colors.HEADER + "[Rendering]" + colors.ENDC)
    actual = renderer.render(ast)
    if actual == example["html"]:
        passed += 1
        catStats[current_section][0] += 1
        if args.t:
            if not args.f:
                print("Test #" + str(args.t.split(",")[i]))
        else:
            if not args.f:
                print("Test #" + str(i + 1))
        if not args.f:
            print(colors.OKGREEN + "tick" + colors.ENDC)
        if args.d:
            CommonMark.dumpAST(ast)
        if args.p or args.d and not args.np:
            print(
                colors.OKBLUE
                + "=== markdown ===============\n"
                + colors.ENDC
                + showSpaces(example["markdown"])
                + colors.OKBLUE
                + "\n=== expected ===============\n"
                + colors.ENDC
                + showSpaces(example["html"])
                + colors.OKBLUE
                + "\n=== got ====================\n"
                + colors.ENDC
                + showSpaces(actual)
            )
    else:
        failed += 1
        catStats[current_section][1] += 1
        if args.t:
            print("Test #" + str(args.t.split(",")[i]))
        else:
            print("Test #" + str(i + 1))
        print(colors.FAIL + "cross" + colors.ENDC)
        if args.d:
            CommonMark.dumpAST(ast)
        if not args.np or args.f:
            print(
                colors.WARNING
                + "=== markdown ===============\n"
                + colors.ENDC
                + showSpaces(example["markdown"])
                + colors.WARNING
                + "\n=== expected ===============\n"
                + colors.ENDC
                + showSpaces(example["html"])
                + colors.WARNING
                + "\n=== got ====================\n"
                + colors.ENDC
                + showSpaces(actual)
            )

print(str(passed) + " tests passed, " + str(failed) + " failed")

endTime = time.clock()
runTime = endTime - startTime

if args.s:
    for i in catStats.keys():
        per = catStats[i][0] / catStats[i][2]
        print(colors.HEADER + "[" + i + "]" + colors.ENDC + "\t" + str(per * 100) + "% Passed")

print("runtime: " + str(runTime) + "s")
