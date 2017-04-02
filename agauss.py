# gaussian model in wavelength space using Angstrom units
# just calls calcGaussianLine

def agauss(energyArray, params, spectrumNumber, fluxArray, fluxErrArray, initString):

	# convert the energy from keV to Angstroms. Need to make sure that we are
	# in increasing order of wavelength to be on the safe side.

	nE = len(energyArray)

	angstromArray = []

	for i in range(0, nE):
		