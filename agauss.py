# gaussian model in wavelength space using Angstrom units
# just calls calcGaussianLine

from Numerics import KEV_TO_A
import calcLines

def agauss(energyArray, params, spectrumNumber, fluxArray, fluxErrArray, initString):

	# convert the energy from keV to Angstroms. Need to make sure that we are
	# in increasing order of wavelength to be on the safe side.

	nE = len(energyArray)
	angstromArray = []

	for i in range(0, nE):
		angstromArray.append(KEV_TO_A / energyArray[nE - 1 - i])

	crtLevel = 1.0e-6
	lineParams = list(params[1])

	angstromFluxArray = []
	calcLines.calcLine(angstromArray, params[0], lineParams, 1.0, crtLevel, 0, False, angstromFluxArray)

	fluxArray.resize(energyArray.size()-1);
	for i in range(0, nE - 1):
		fluxArray[i] = angstromFluxArray[nE - 2 - i]
	fluxErrArray = []

