

def to_bin(sample):
	#print(sample)
	res = "{0:012b}".format(int(sample, 16))
	print('Binary: ' + res)
	#dec = twos_comp(int(res, 2), len(res))

	return res

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is

"""
samp = 'AFF91FF9'
d0 = 227
d1 = 7
b0 = to_dec(d0)
b1 = to_dec(d1)


concat = "".join([b0[4:8], b1])

p1 = twos_comp(int(concat,2), len(concat))

print(concat)
print(p1)

"""
print('Input Hex Value (type "exit" to escape): ')
while True:
	print('Hex Value: ')
	inp = input()
	if inp == "exit":
		break
	else:
		b = to_bin(str(inp))
		print('Signed Int: ' + str(twos_comp(int(b, 2), len(b))))

