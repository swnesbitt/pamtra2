import os
import shlex

import sys
from glob import glob

import numpy
import setuptools
from Cython.Build import cythonize
from numpy.distutils.core import setup
from numpy.distutils.extension import Extension
from numpy.distutils.misc_util import Configuration


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# try:
#     os.environ['LDFLAGS'] += " -shared"
# except KeyError:
#     os.environ['LDFLAGS'] = " -shared"

kw = {}
if sys.platform == 'darwin':
    kw['extra_link_args'] = ['-undefined dynamic_lookup', '-bundle']

library_dirs = ['~/.local/lib/', '/usr/local/lib/', '/opt/local/lib/', '/opt/homebrew/lib/']

def configuration(parent_package='', top_path=None):

    config = Configuration(
        'pamtra2',
        parent_package,
        top_path,
        version='0.1',
        author="Pamtra Team",
        author_email="maximilian.maahn@colorado.edu",
        description="atmospheric microwace passive"
                    " and active instrument simulator",
        license="GPL v3",
        python_requires='>=3.5',
        url='https://github.com/maahn/pamtra2',
        download_url='https://github.com/maahn/pamtra2/'
                     'releases/download/0.1/pamtra2-0.1.zip',
        long_description=read('README.rst'),
        classifiers=[
            "Development Status :: 3 - Alpha",
            "License :: OSI Approved :: GPL v3 License",
            "Operating System :: OS Independent",
            "Programming Language :: Fortran",
            "Programming Language :: Python",
            "Intended Audience :: Science/Research",
            "Topic :: Scientific/Engineering :: Atmospheric Science",
        ]
    )

    return config


pamgasabs_path = 'libs/pamgasabs/pamgasabs'
pamgasabs = Extension(
    'pamtra2.libs.pamgasabs.pamgasabs_lib',
    sources=[
        '%s/pamgasabs_lib/pamgasabs_lib.pyf' % pamgasabs_path,
        '%s/pamgasabs_lib/kinds.f90' % pamgasabs_path,
        '%s/pamgasabs_lib/report_module.f90' % pamgasabs_path,
        '%s/pamgasabs_lib/constants.f90' % pamgasabs_path,
        '%s/pamgasabs_lib/gasabs_module.f90' % pamgasabs_path,
        '%s/pamgasabs_lib/rosen98_gasabs.f90' % pamgasabs_path,
        '%s/pamgasabs_lib/mpm93.f90' % pamgasabs_path,
    ], 
    extra_compile_args = [ "-fPIC"],
    **kw)

pyrasim_path = 'libs/pyPamtraRadarSimulator/pyPamtraRadarSimulator'
pyrasim = Extension(
    'pamtra2.libs.pyPamtraRadarSimulator.pyPamtraRadarSimulatorLib',
    sources=[
        '%s/pyPamtraRadarSimulatorLib/pyPamtraRadarSimulatorLib.pyf' %
        pyrasim_path,
        '%s/pyPamtraRadarSimulatorLib/kinds.f90' % pyrasim_path,
        '%s/pyPamtraRadarSimulatorLib/report_module.f90' % pyrasim_path,
        '%s/pyPamtraRadarSimulatorLib/constants.f90' % pyrasim_path,
        '%s/pyPamtraRadarSimulatorLib/dsort.f90' % pyrasim_path,
        '%s/pyPamtraRadarSimulatorLib/convolution.f90' % pyrasim_path,
        '%s/pyPamtraRadarSimulatorLib/viscosity_air.f90' % pyrasim_path,
        '%s/pyPamtraRadarSimulatorLib/random_module.f90' % pyrasim_path,
        '%s/pyPamtraRadarSimulatorLib/rescale_spectra.f90' % pyrasim_path,
        '%s/pyPamtraRadarSimulatorLib/dia2vel.f90' % pyrasim_path,
        '%s/pyPamtraRadarSimulatorLib/radar_simulator.f90' % pyrasim_path,
        '%s/pyPamtraRadarSimulatorLib/radar_spectral_broadening.f90' %
        pyrasim_path,
        '%s/pyPamtraRadarSimulatorLib/radar_spectrum.f90' % pyrasim_path,
        '%s/pyPamtraRadarSimulatorLib/rho_air.f90' % pyrasim_path,
    ],
    library_dirs=library_dirs,
    libraries=['fftw3', 'lapack'],
    extra_compile_args = [ "-fPIC"],
    **kw)

pyramom_path = 'libs/pyPamtraRadarMoments/pyPamtraRadarMoments'
pyramom = Extension(
    'pamtra2.libs.pyPamtraRadarMoments.pyPamtraRadarMomentsLib',
    sources=[
        '%s/pyPamtraRadarMomentsLib/nan.f90' % pyramom_path,
        '%s/pyPamtraRadarMomentsLib/pyPamtraRadarMomentsLib.pyf' % pyramom_path,
        '%s/pyPamtraRadarMomentsLib/kinds.f90' % pyramom_path,
        '%s/pyPamtraRadarMomentsLib/report_module.f90' % pyramom_path,
        '%s/pyPamtraRadarMomentsLib/constants.f90' % pyramom_path,
        '%s/pyPamtraRadarMomentsLib/convolution.f90' % pyramom_path,
        '%s/pyPamtraRadarMomentsLib/dsort.f90' % pyramom_path,
        '%s/pyPamtraRadarMomentsLib/hildebrand_sekhon.f90' % pyramom_path,
        '%s/pyPamtraRadarMomentsLib/smooth_savitzky_golay.f90' % pyramom_path,
        '%s/pyPamtraRadarMomentsLib/calc_moments.f90' % pyramom_path,
    ],
    library_dirs=library_dirs,
    libraries=['fftw3', 'lapack'],
    extra_compile_args = [ "-fPIC"],
    **kw)

refractiveIndex_path = 'libs/refractiveIndex/refractiveIndex'
meteo_si_path = 'libs/meteo_si/meteo_si'

singleScattering_path = 'libs/singleScattering'
cMie = Extension(
    name = "pamtra2.libs.singleScattering.cMie",
    sources = ["%s/Mie/cython/cMie.pyx" % singleScattering_path,
             "%s/Mie/src/cMie.c" % singleScattering_path],
    include_dirs = [numpy.get_include()],
    extra_compile_args = ["-O3", "-ffast-math",
                          "-Wall", "-lm", "-fPIC", "-std=c99"],
    language='c'
)

fTMat = Extension(
    name = 'pamtra2.libs.singleScattering.fTMat',
    sources = [
        '%s/Tmatrix/ampld.lp.f90' % singleScattering_path,
        '%s/Tmatrix/lpd.f90' % singleScattering_path,
        '%s/Tmatrix/pytmatrix.pyf' % singleScattering_path,
    ],
    extra_compile_args = [ "-fPIC"],
    **kw)


if __name__ == "__main__":

    setup(
        configuration=configuration,
        packages=['pamtra2', 'pamtra2.hydrometeors',
                  'pamtra2.instruments', 'pamtra2.libs',
                  'pamtra2.libs.pamgasabs',
                  'pamtra2.libs.pyPamtraRadarSimulator',
                  'pamtra2.libs.pyPamtraRadarMoments',
                  'pamtra2.libs.refractiveIndex',
                  'pamtra2.libs.singleScattering',
                  'pamtra2.libs.meteo_si','pamtra2.importer'
                  ],
        package_dir={
            'pamtra2': 'src/pamtra2' ,
            'pamtra2.libs.pamgasabs': pamgasabs_path,
            'pamtra2.libs.pyPamtraRadarSimulator': pyrasim_path,
            'pamtra2.libs.pyPamtraRadarMoments': pyramom_path,
            'pamtra2.libs.refractiveIndex': refractiveIndex_path,
            'pamtra2.libs.meteo_si': meteo_si_path,
            'pamtra2.libs.singleScattering': '%s/singleScattering' %
            singleScattering_path,
        },
        package_data={
            # Don't aks me why, but I need an extra random character in front
            # of the *dat files...
            'pamtra2.libs.refractiveIndex': ['*.dat'],
            'pamtra2.libs.singleScattering': ['*.dat'],
        },
        platforms=['any'],
        install_requires=['numpy', 'scipy', 'xarray', 'dask[complete]', 'numba',
                  'cython'],
        build_requires=['numpy', 'cython'],
        setup_requires=["pytest-runner"],
        tests_require=["pytest"],
        ext_modules=cythonize(
            [pamgasabs, pyrasim, pyramom, cMie, fTMat]),

    )
