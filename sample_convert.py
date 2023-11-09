

def get_dec(sample):
	print(sample)
	res = "{0:012b}".format(int(sample, 16))
	print(res)
	dec = twos_comp(int(res, 2), len(res))

	return dec

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is

"""
samp = 'AFF91FF9'
#output = to_dec(samp[1:4])
#output = to_dec(samp[5:8])

print(to_dec(samp[1:4]))
print(to_dec(samp[5:8]))
"""