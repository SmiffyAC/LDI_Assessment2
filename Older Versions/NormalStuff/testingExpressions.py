print ("hello" + " " + "world")
print ("foo" + "bar" == "foobar")
print ("10 corgis" != "10" + "corgis")
print ("5" + "5")
print (True + False)
print (1 == 1.0)
print (2 == 1.0)
print (True or False)
print (False or True)
print (not True)

# if statement - python example
print("\nIF STATEMENT----------------------------")
x = 41

if x > 10:
  print("Above ten,")
  if x > 20:
    print("and also above 20!")
  else:
    print("but not above 20.")

# while look with break - python example
print("\nWHILE LOOP------------------------------")
i = 1
while i < 6:
  print(i)
  if i == 3:
    break
  i += 1

print("\n")


ans = not (5 - 4 > 3 * 2 == (not False))

print(ans)