def solve():
	file_in = open("8.txt", "r")
	arr = file_in.read().split('\n')
	file_in.close()

	for i in range(len(arr)): #aes block length is 128 bits or 32 hex
		blocks = set()
		j = 0
		while j + 31 < len(arr[i]):
			block = arr[i][j:j+32]
			if block in blocks:
				print("Line #" + str(i) + " has been encrypted with ECB: " + arr[i])
				break
			blocks.add(block)
			j += 32

solve()