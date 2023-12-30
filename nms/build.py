import os
from setuptools import setup
from torch.utils.cpp_extension import CUDAExtension, BuildExtension
import torch

# Define sources and headers
sources = ['nms/src/nms.c']
headers = ['nms/src/nms.h']
defines = []
with_cuda = False

# Check if CUDA is available and modify sources and headers accordingly
if torch.cuda.is_available():
    print('Including CUDA code.')
    sources += ['nms/src/nms_cuda.c']
    headers += ['nms/src/nms_cuda.h']
    defines += [('WITH_CUDA', None)]
    with_cuda = True

this_file = os.path.dirname(os.path.realpath(__file__))
print(this_file)

# Include the CUDA kernel object file if CUDA is available
extra_objects = []
if with_cuda:
    extra_objects = ['nms/src/cuda/nms_kernel.cu.o']
    extra_objects = [os.path.join(this_file, fname) for fname in extra_objects]

# Define the extension module
ext_modules = [
    CUDAExtension(
        name='_ext.nms', 
        sources=sources, 
        include_dirs=[os.path.join(this_file, 'nms/src')],
        define_macros=defines,
        extra_compile_args={'cxx': [], 'nvcc': []},
        extra_objects=extra_objects
    )
]

# Setup function
def build(setup_kwargs):
    setup_kwargs.update({
        'ext_modules': ext_modules,
        'cmdclass': {'build_ext': BuildExtension}
    })

if __name__ == '__main__':
    setup(
        name='nms_extension',
        version='0.1',
        description='NMS Build Script',
        packages=['nms'],
        ext_modules=ext_modules,
        cmdclass={
            'build_ext': BuildExtension.with_options(no_python_abi_suffix=True)
        }
    )
