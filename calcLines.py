import BinarySearch
import Numerics
import math

GAUSS =  0
LORENTZ = 1
VOIGT = 2

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
			fractionInsideRange = lineFraction(lineShape, efirst, ecenter, lineParams, qspeedy) / 2
			if ecenter > elast:
				ielow = nE - 2
				alow = lineFraction(lineShape, elast, ecenter, lineParams, qspeedy)
				fractionInsideRange -= alow / 2 									

			# Do the low energy part of the line
			lineSum = 0.0
			ahi = 0.0

			while ielow >= 0:
				ahi = lineFraction(lineShape, energyArray[ielow], ecenter, lineParams, qspeedy)
				fract = (ahi - alow) / 2

				fluxArray[ielow] += fract * lineflux;
				lineSum += fract

				if (fractionInsideRange - lineSum) < crtLevel:
					# Too many sigma away so stop now and add the rest of the line into this
					# bin. Not strictly correct but shouldn't matter and ensures that the total
					# flux is preserved.
					fluxArray[ielow] += (fractionInsideRange - lineSum) * lineflux
					ielow = 0

				alow = ahi
				ielow -= 1

		# If the line center is above the last bin then don't calculate 
		# the upper part of the line. If line center is below first bin then 
		# just calculate the part of the line within energy range.

		if ecenter <= elast:
			alow = 0.0
			ielow = icen
			fractionInsideRange = lineFraction(lineShape, elast, ecenter, lineParams, qspeedy) / 2

			if ecenter <  efirst:
				ielow = 0
				alow = lineFraction(lineShape, energyArray[ielow], ecenter, lineParams, qspeedy)
				fractionInsideRange -= alow / 2

			# Do the high energy part of the line

			lineSum = 0.0;
			ahi = 0.0

			while ielow < nE - 1:
				ahi = lineFraction(lineShape, energyArray[ielow+1], ecenter, lineParams, qspeedy)
				fract = (ahi - alow) / 2
				fluxArray[ielow] += fract * lineflux
				lineSum += fract

				if (fractionInsideRange - lineSum) < crtLevel:
					# Too many sigma away so stop now and add the rest of the Gaussian into this
					# bin. Not strictly correct but shouldn't matter and ensures that the total
					# flux is preserved.
					fluxArray[ielow] += (fractionInsideRange - lineSum) * lineflux
					ielow = nE
				alow = ahi
				ielow += 1


def lineFraction(lineShape, energy, ecenter, lineParams, qspeedy):
	first = True
	saveEcenter = 0
	saveWidth = 0
	lnorm = 0

	if lineShape == GAUSS:
		return gaussFraction(math.fabs(energy - ecenter) / lineParams[0], qspeedy)
	elif lineShape == LORENTZ:
		if first or ecenter != saveEcenter or saveWidth != lineParams[0]:
			saveEcenter = ecenter;
			saveWidth = lineParams[0];
			lnorm = 1.0 / (math.pi / 2.0 - atan(-2.0 * ecenter / lineParams[0]))
			first = False

		lfrac = lorentzFraction(math.fabs(energy - ecenter) / lineParams[0], qspeedy)
		return lfrac * lnorm
	elif lineShape == VOIGT:
		return voigtFraction(energy, ecenter, lineParams[0], lineParams[1], qspeedy)
	else:
		return 0.0


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


def voigtFraction(energy, ecenter, sigma, gamma, qspeedy):

	# Function to return the integral of a Voigt(ecenter,sigma,gamma) distribution 
	# from -energy to +energy.
	# If qspeedy=true interpolates on a previously calculated grid of calculations
	# while if qspeedy=false then does calculation each time.

	# for now use a pseudo-Voigt approximation (good to 1%) which is just a sum of a 
	# Gaussian and a Lorentzian. Reference is Ida, T, Ando, M and Toraya, H (2000), 
	# "Extended pseudo-Voigt function for approximating the Voigt profile",
	# Journal of Applied Crystallography 33 (6): 1311–1316.

	gaussValue = 0
	lorentzValue = 0
	if sigma > 0.0:
		gaussValue = gaussFraction(math.fabs(energy - ecenter) / sigma, qspeedy)
	if gamma > 0.0:
		lorentzValue = lorentzFraction(math.fabs(energy - ecenter) / gamma, qspeedy)

	if sigma == 0.0:
		return lorentzValue
	if gamma == 0.0:
		return gaussValue

	# 2sqrt(2ln(2)) = 2.35482

	fG = 2.35482 * sigma
	fL = 2.0 * gamma

	f = fG**5 + 2.69269*fG**4*fL + 2.42843*fG**3*fL*fL + .47163*fG*fG*fL**3 + 0.07842*fG*fL**4 + fL**5
	f = f ** 0.2
	
	fLof = fL / f
	eta = 1.36603*fLof - 0.47719*fLof*fLof + 0.11116*fLof*fLof*fLof

	return eta * lorentzValue + (1.0 - eta) * gaussValue



	