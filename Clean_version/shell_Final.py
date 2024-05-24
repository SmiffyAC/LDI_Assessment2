import Basic_final

while True:
	text = input('\nshell > ')
	if text.strip() == "": continue
	result, error = Basic_final.run('<stdin>', text)

	if error:
		print(error.as_string())
	elif result:
		if len(result.elements) == 1:
			print(repr(result.elements[0]))
		else:
			print(repr(result))