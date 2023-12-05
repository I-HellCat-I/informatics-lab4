from Task1 import *
from Task3 import parse

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    convertJSONToXML1("Zanatiya.json", "answer.xml")
    convertJSONtoXML2("Zanatiya.json", "answer2.xml")
    convertJSONtoXML3("Zanatiya.json", "answer3.xml")
    convertJSONToXML4("Zanatiya.json", "answer4.xml")
    #print(''.join(open('Zanatiya.json').readlines()).replace('\n', '').replace(' ', ''))
    #print(parse(''.join(open('Zanatiya.json').readlines()).replace('\n', '').replace(' ', '')))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
