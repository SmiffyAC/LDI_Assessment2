from claude_version import run

code = '''
var x = 10
var y = 20
var result = x + y
print(result)

var name = "John"
var age = 25
print("My name is " + name + " and I am " + str(age) + " years old.")

if (x > y):
    print("x is greater than y")
else:
    print("x is not greater than y")

var i = 0
while (i < 5):
    print(i)
    i = i + 1
'''

result, error = run(code)

if error:
    print(error)
else:
    print(result)