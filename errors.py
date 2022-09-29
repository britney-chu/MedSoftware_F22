def calc_square_root(n):
	try:
		from my_calculator import sqrt
	except ModuleNotFoundError:
		print("The my_calculator module was not found." +
			  "Loading Python math library instead.")
		from math import sqrt
	answer = sqrt(n)
	return answer


def function_name():
	try:
		x = 1 + "hello"
	except TypeError:
		print("you cannot add a string to an integer, silly goose!")


def main():
	print(calc_square_root(2))
	function_name()

if __name__ == "__main__":
	main()
