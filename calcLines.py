

def calcLine(energyArray, ecenter, lineParams, lineflux, crtLevel, lineShape, qspeedy, fluxArray):
	ecenterArray = list(ecenter)
	lineParamsArray = list(lineParams)
	linefluxArray = list(lineflux)


def calcManyLines(energyArray, ecenterArray, lineParamsArray, linefluxArray, crtLevel, lineShape, qspeedy, fluxArray):
	# Find the bins containing the line centers. This assumes that the ecenter
 	# array is in increasing order of energy. If the center energy falls outside
 	# the energy array then lineCenterBin will be set to -1. Otherwise
 	# energyArray[lineCenterBin] < ecenterArray <= energyArray[lineCenterBin+1]

 	lineCenterBin = []