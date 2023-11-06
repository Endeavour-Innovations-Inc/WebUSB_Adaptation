def get_sample1(packed)
	sample1 = get_dec(pack1)
	return sample1

def get_sample2(packed)
	sample2 = get_dec(pack2)
	return sample2

def get_dec(sample):
	res = "{0:012b}".format(int(sample, 16))
	print(res)
	dec = twos_comp(int(res, 2), len(res))

	return dec

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is

samp = '1F'
output = get_dec(samp)

print(output)