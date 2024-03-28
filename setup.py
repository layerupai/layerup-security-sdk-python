from setuptools import setup, find_packages

setup(
    name='LayerupSecurity',
    version='1.1.1',
    author='Layerup',
    author_email='pypi@uselayerup.com',
    description='A Python wrapper for the Layerup Security API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/layerupai/layerup-security-sdk-python',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7',
)
