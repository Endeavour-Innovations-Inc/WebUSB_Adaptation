

def to_dec(sample):
	print(sample)
	res = "{0:08b}".format(sample)
	#print(res)
	#dec = twos_comp(int(res, 2), len(res))

	return res

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is


samp = 'AFF91FF9'
d0 = 15
d1 = 249
#b0 = to_dec(d0)
#b1 = to_dec(d1)

concat = '011111110011'

p1 = twos_comp(int(concat, 2), 12)

print(concat)
print(p1)


