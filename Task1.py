from collections import deque
from json2xml import json2xml
from json2xml.utils import readfromjson
import re
import ply.lex as lex
import ply.yacc as yacc



def convertJSONToXML1(filename, towrite):
    answer = []
    with open(filename) as f:
        stack = deque([])
        tabs = 1
        answer.append('<Schedule>\n')
        stack.appendleft('</Schedule>\n')
        for s in f.readlines()[1:-1]:
            s = s.strip()
            name = ''
            tmp = ''
            fl = False
            isList = False
            isVal = False
            isDict = False
            if s[0] == '}' or s[0] == ']':
                answer.append(stack.popleft())
                tabs -= 1
                continue
            for x in range(len(s)):
                if s[x] == '"':
                    fl = not fl
                    continue
                if fl:
                    tmp += s[x]
                    continue
                if s[x] == ',':
                    break
                if isVal and s[x] == '{':
                    stack.appendleft(f'{tabs * 4 * " "}</attribute>\n')
                    tabs += 1
                    isDict = True
                    break
                if isVal and s[x] == '[':
                    isList = True
                    stack.appendleft(f'{tabs * 4 * " "}</list>\n')
                    tabs += 1
                if isVal and s[x] != " ":
                    tmp += s[x]
                if s[x] == ":":
                    name = tmp
                    tmp = ''
                    isVal = True
            if isDict:
                answer.append(f'{(tabs - 1) * 4 * " "}<attribute name="{name}">\n')
            elif isList:
                answer.append(f'{(tabs - 1) * 4 * " "}<list name="{name}">\n')
            elif '</list>' in stack[0]:
                answer.append(f'{tabs * 4 * " "}<item type="{"int" if s.strip(",").isdigit() else "str"}">{s.strip(",")}</item>\n')
            else:
                answer.append(f'{tabs * 4 * " "}<field name="{name}" type="{"int" if tmp.isdigit() else "str"}">{tmp}</field>\n')

        answer.append(stack.popleft())
        with open(towrite, 'w') as tw:
            tw.writelines(answer)


def convertJSONtoXML2(fn, towrite):
    with open(towrite, 'w') as tw:
        tw.writelines(json2xml.Json2xml(readfromjson(fn)).to_xml())


def convertJSONtoXML3(fn, towrite):
    pattern = r'^"([^"]+)"\s*:\s*(\S[^"]*)'
    answer = []
    with open(fn) as f:
        stack = deque([])
        tabs = 1
        answer.append('<Schedule>\n')
        for s in f.readlines()[1:-1]:
            s = s.strip()
            try:
                name, args = re.findall(pattern, s)[0]
                args = args.strip('"').rstrip(",")
                if args == '{':
                    stack.appendleft(f'{tabs * 4 * " "}</attribute>\n')
                    answer.append(f'{tabs * 4 * " "}<attribute name="{name}">\n')
                    tabs += 1
                elif args == '[':
                    stack.appendleft(f'{tabs * 4 * " "}</list>\n')
                    answer.append(f'{tabs * 4 * " "}<list name="{name}">\n')
                    tabs += 1
                else:
                    answer.append(f'{tabs * 4 * " "}<field name="{name}" type="{"int" if args.isdigit() else "str"}">{args}</field>\n')
            except IndexError:
                if s[0] not in {'}', ']'}:
                    answer.append(f'{tabs * 4 * " "}<item type="{"int" if s.strip(",").isdigit() else "str"}">{s.strip(",")}</item>\n')
                    continue
                answer.append(stack.popleft())
                tabs -= 1
        answer.append('</Schedule>\n')
    with open(towrite, 'w') as tw:
        tw.writelines(answer)


def convertJSONToXML4(fn, towrite):
    answer = []
    with open(fn) as f:
        stack = deque([])
        tabs = 1
        answer.append('<Schedule>\n')
        stack.appendleft('</Schedule>\n')
        pt = re.compile(r'(:?(:?},\s*)?(".+?")\s*:\s*(:?{|(:?".+?")|\d+|(:?[[](:?.+[,]?)[]],?)))', re.DOTALL)
        listpt = re.compile(r'(:?(:?(:?".+?")|\d+),?\s*)+?')
        s = ''.join(f.readlines())
        razgresti = pt.findall(s)
        print(razgresti)
        for x in razgresti:
            if x[0][0] in {'}', ']'}:
                tabs -= 1
                answer.append(stack.popleft())
            if x[3][0] not in {'[', '{'}:
                args = x[3].strip('"')
                answer.append(f'{tabs * 4 * " "}<field name={x[2]} type="{"int" if args.isdigit() else "str"}">{args}</field>\n')
            elif x[3][0] == '{':
                stack.appendleft(f'{tabs * 4 * " "}</attribute>\n')
                answer.append(f'{tabs * 4 * " "}<attribute name={x[2]}>\n')
                tabs += 1
            else:
                stack.appendleft(f'{tabs * 4 * " "}</list>\n')
                answer.append(f'{tabs * 4 * " "}<list name={x[2]}>\n')
                tabs += 1
                print(x[-1])
                print(listpt.findall(x[-1]))
                for i in listpt.findall(x[-1]):
                    a = i[1].strip('"')
                    answer.append(f'{tabs * 4 * " "}<item type="{"int" if a.isdigit() else "str"}">{a}</item>\n')
        while stack:
            tabs -= 1
            answer.append(stack.popleft())
        with open(towrite, 'w') as tw:
            tw.writelines(answer)
