import BinarySearch
import Numerics
import math

def calcLine(energyArray, ecenter, lineParams, lineflux, crtLevel, lineShape, qspeedy, fluxArray):
	ecenterArray = list(ecenter)
	lineParamsArray = list(lineParams)
	linefluxArray = list(lineflux)


def calcManyLines(energyArray, ecenterArray, lineParamsArray, linefluxArray, crtLevel, lineShape, qspeedy, fluxArray):
	# Find the bins containing the line centers. This assumes that the ecenter
 	# array is in increasing order of energy. If the center energy falls outside
 	# the energy array then lineCenterBin will be set to -1. Otherwise
 	# energyArray[lineCenterBin] < ecenterArray <= energyArray[lineCenterBin+1]

 	lineCenterBin = BinarySearch.Binarysearch(energyArray, ecenterArray)

 	efirst = energyArray[0]
 	nE = len(energyArray)
 	elast = energyArray[nE - 1]

 	# Loop around the lines

 	for iline in range(0, len(ecenterArray)):
 		icen = lineCenterBin[iline]
 		ecenter = ecenterArray[iline]
 		lineParams = lineParamsArray[iline]
 		lineflux = linefluxArray[iline]


 		# first do case of zero width line. assume for the moment that this occurs
    	# if all the lineParams are zero
		
		deltaFunction = True

		for i in range(0, len(lineParams)):
			if lineParams[i] != 0:
				deltaFunction = False
				break

			if deltaFunction == True:
				if icen != -1:
					fluxArray[icen] += lineflux
					continue

		# If the line center is below first bin then don't calculate the 
		# lower part of the line. If line center is above the first bin
		# then just calculate part of line within the energy range.

		if ecenter >= efirst:
			ielow = icen
			alow = 0.0
			#################################


def gaussFraction(deltasigma, qspeedy):

	# Function to return the integral of a Gaussian(0,1) distribution from 
	# -deltasigma to +deltasigma
	# If qspeedy=true interpolates on a previously calculated grid of erf calculations
	# while if qspeedy=false then calls erf each time.

	GaussMaxStep = 1200
	GaussMax = 6
	GaussStep = GaussMax / GaussMaxStep

	tabErf = []
	first = True

	# if the first time through then calculate the erf grid on which we
	# will interpolate

	if qspeedy and first:
		for i in range(0, GaussMaxStep + 1):
			tabErf[i] = math.erf(i * GaussStep / Numerics.SQRT2)
		first = False

	# how many sigmas away we are
	x = math.fabs(deltasigma)

	if qspeedy:
		# Now interpolate from the table
		index = x // GaussStep

		# If we're past the edge of the tabulated data return 1.0
		if index >= GaussMaxStep:
			return 1.0

		remainder = (x - index * GaussStep) * (1.0 / GaussStep)

		# Do the interpolation
		return (1.0 - remainder) * tabErf[index] + remainder * tabErf[index + 1]
	else:
		return math.erf(x / Numerics.SQRT2)


def lorentzFraction(deltasigma, qspeedy):

	# Function to return the integral of a Lorentzian(0,1) distribution from 
	# -deltasigma to +deltasigma. There is an additional normalization factor
	# which depends on the line energy and width of 1/(pi/2 - arctan(-2*E0/W))
	# and should be applied by the routine calling lorentzFraction.
	# If qspeedy=true interpolates on a previously calculated grid of calculations
	# while if qspeedy=false then does calculation each time.

	LorentzMaxStep = 1200
	LorentzMax = 6
	LorentzStep = LorentzMax / LorentzMaxStep

	tabLor = []
	first = True

	# if the first time through then calculate the grid on which we
	# will interpolate

	if qspeedy and first:
		for i in range(0, LorentzMaxStep + 1):
			tabLor[i] = 2 * math.atan(2 * i * LorentzStep)
		first = False

	# how many sigmas away we are
	x = math.fabs(deltasigma)

	if qspeedy:
		index = x // LorentzStep

		# If we're past the edge of the tabulated data return 1.0.
		if index >= LorentzMaxStep:
			return 1.0

		remainder = (x - index * LorentzStep) * (1.0 / LorentzStep)

		# Do the interpolation
		return 2 * (1.0 - remainder) * tabLor[index] + remainder * tabLor[index + 1]
	else:
		return 2 * math.atan(2 * x)





	