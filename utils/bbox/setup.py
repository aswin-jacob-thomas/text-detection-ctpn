from distutils.core import setup

import numpy as np
from Cython.Build import cythonize

numpy_include = np.get_include()
setup(ext_modules=cythonize("./utils/bbox/bbox.pyx"), include_dirs=[numpy_include])
setup(ext_modules=cythonize("./utils/bbox/nms.pyx"), include_dirs=[numpy_include])
