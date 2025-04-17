from setuptools import setup, find_packages

def read_requirements(file_path):
    """
    Reads a requirements.txt file and returns a list of dependencies,
    removing comments, '-e', 'git+', and newline characters.
    """
    with open(file_path, 'r') as f:
        req = [line.replace('\n', '').strip() for line in f if line.strip() and not line.startswith('#')]
        for i in range(len(req)):
            if req[i].startswith('-e '):
                req[i] = req[i][3:]
            if req[i].startswith('git+'):
                req[i] = req[i][4:]
        return req

setup(
    name='mlproject',
    version='0.0.1',
    author='Ashok Kumar',
    author_email='ap86963163@gmail.com',
    packages=find_packages(),
    install_requires=read_requirements('requirements.txt'),
    description='Hands-on ML project with mini-projects and examples covering core machine learning workflows.',
    long_description=open('README.md', encoding='utf-8').read().strip(),
    long_description_content_type='text/markdown',
    url='https://github.com/Ashok-Prajapati2/mlproject',
    license='GPL-3.0',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)