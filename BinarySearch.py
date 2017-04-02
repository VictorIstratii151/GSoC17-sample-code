# Binary search on a RealArray to return the indices of the element immediately
# before the input values assuming the input values are in ascending order.

def Binarysearch(x, y):
	nX = len(x)
	nY = len(y)
	elementArray = []

	for i in range(0, nY):
		elementArray[i] = -1

	if nX == 1:
		return elementArray

	low = 0;
	xmin = x[0];
	xmax = x[nX - 1];

	for i in range(0, nY):
		yval = y[i]

		if yval > xmax:
			break
		# catch the special case of the y value being at the minimum of the range
		# we have to do this otherwise elementArray ends up incorrectly as -1.

		if yval == xmin:
			elementArray[i] = 0
			break

		if yval > xmin:
			high = nX - 1
			bisearch = low

			while (high - low) > 1:
				bisearch = (low + high) // 2
				if yval > x[bisearch - 1]:
					low = bisearch
				else:
					high = bisearch

			if yval > x[bisearch]:
				bisearch = high
			else:
				bisearch = low

		elementArray[i] = bisearch - 1

	return elementArray




	