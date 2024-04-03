import setuptools

name='visla'

with open('readme.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name=name,  
    version='0.0.0',
    scripts=[f'bin/{name}'] ,
    author='Gabriel H. Brown',
    author_email='gabriel.h.brown@gmail.com',
    description='Easy and attractive visualizations of sparse matrices and graphs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=f'https://github.com/ghbrown/{name}',
    packages=setuptools.find_packages(),
    #include_package_data = True, #include non-Python files specified in MANIFEST.in
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
    ],
    keywords=[
        'graph',
        'visualize',
        'sparse',
        'matrix',
    ],
    install_requires=[
        'numpy',
        'scipy',
        'pygraphviz',
        'matplotlib',
        'cmasher',
        'ssgetpy'
    ],
 )
