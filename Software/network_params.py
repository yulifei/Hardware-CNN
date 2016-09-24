import math
# General Network Parameters
INPUT_SIZE = 28 # dimension of square input image
NUM_KERNELS = 10
KERNEL_SIZE = 9 # square kernel
FEATURE_SIZE = INPUT_SIZE - KERNEL_SIZE + 1 # The dimension of the convolved image

# General Bitwidths
NN_WIDTH = 16
NN_BITWIDTH = NN_WIDTH - 1


# Rect Linear


# Sub sampling
NEIGHBORHOOD_SIZE = 4
NH_VECTOR_WIDTH = NEIGHBORHOOD_SIZE*NN_WIDTH
NH_VECTOR_BITWIDTH = NH_VECTOR_WIDTH - 1 
NUM_NH_LAYERS = int(math.ceil(math.log(NEIGHBORHOOD_SIZE,2)))
#NUM_NH_LAYERS PNUM_NH_LAYERS
POOL_OUT_WIDTH = NN_WIDTH + NUM_NH_LAYERS 
POOL_OUT_BITWIDTH = POOL_OUT_WIDTH - 1 
MEAN_DIVSION_CONSTANT = str(POOL_OUT_WIDTH) + "'d" + str(NEIGHBORHOOD_SIZE)
# POOL_RESET= 1 # uncomment to add reset signal to sub sampleing/pooling adder tree
POOL_TREE_PAD = POOL_OUT_WIDTH - NN_WIDTH
# Softmax 
SOFTMAX_IN_VECTOR_LENGTH = ((FEATURE_SIZE * FEATURE_SIZE) / NEIGHBORHOOD_SIZE ) * NUM_KERNELS  # the number of inputs to the softmax layer
NUM_CLASSES = 4 # number of output classes for the entire nn, MUST BE A POWER OF 2!!! set unneeded class inputs to 0

# Matrix multiply (for Softmax)
NUM_INPUT_IM = 1 # The number of images input to the layer at a time
NUM_INPUT_N  = (NUM_KERNELS * FEATURE_SIZE * FEATURE_SIZE )# The number of input neurons to the layer
NUM_OUTPUT_N = NUM_CLASSES
FFN_WIDTH = NN_WIDTH # The width of the inputs to the feed forward network. Should be the same as the output width of the softmax layer.
FFN_BITWIDTH = (FFN_WIDTH - 1)
FFN_OUT_WIDTH = (FFN_WIDTH * 2) + int(math.ceil(math.log(NUM_INPUT_N,2))) # The width of the outputs of the feed forward network
FFN_OUT_BITWIDTH = (FFN_OUT_WIDTH - 1)
SUM_WIRE_LEN = ( NUM_INPUT_N * 2 ) - 1 # The number of indexes in the adder tree vector

# Normalization (for Softmax)
NORM_IN_WIDTH = FFN_OUT_WIDTH
NORM_IN_BITWIDTH = NORM_IN_WIDTH - 1
NUM_NORM_LAYERS = int(math.ceil(math.log(NUM_CLASSES,2)))
NORM_OUT_WIDTH = NORM_IN_WIDTH + NUM_NORM_LAYERS
NORM_OUT_BITWIDTH = NORM_OUT_WIDTH - 1
# NORM_RESET = 1 # uncomment to add reset signal to normalization adder tree
ADDER_TREE_PAD = NORM_OUT_WIDTH - NORM_IN_WIDTH




"""
LOG2 = "LOG2(x) \
    (x <= 2) ? 1 : \
    (x <= 4) ? 2 : \
    (x <= 8) ? 3 : \
    (x <= 16) ? 4 : \
    (x <= 32) ? 5 : \
    (x <= 64) ? 6 : \
    (x <= 128) ? 7 : \
    (x <= 256) ? 8 : \
    ((x) <= 512) ? 9 : \
    (x <= 1024) ? 10 : \
    (x <= 2048) ? 11 : \
    (x <= 4096) ? 12 : \
    (x <= 8192) ? 13 : \
    (x <= 16384) ? 14 : \
    (x <= 32768) ? 15 : \
    -100000"
"""

macroList = []
blacklist = ['__', 'math', 'macroList','blacklist']

for k, v in list(locals().iteritems()):
    if not any(substring in k for substring in blacklist):
        macroList.append((k,v))

with open("../Hardware/network_params.h", 'w') as f:
    for macro in macroList:
        f.write("`define " + str(macro[0]) + ' ' + str(macro[1]) + '\n')

    