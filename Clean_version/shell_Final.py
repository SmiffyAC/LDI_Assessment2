import Basic_final

while True:
	# Ask the user for input
	text = input('\n>>> ')
	# If the user entered nothing, continue
	if text.strip() == "": continue
	# Use <stdin> as a placeholder for the filename - calls the run function from Basic_final.py
	result, error = Basic_final.run('<stdin>', text)

	if error:
		# If there is an error, print it
		print(error.as_string())
	elif result:
		# If there is a result, print it
		if len(result.elements) == 1:
			print(repr(result.elements[0]))
		else:
			print(repr(result))