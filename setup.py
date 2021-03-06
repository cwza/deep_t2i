from pkg_resources import parse_version
from configparser import ConfigParser
import setuptools
assert parse_version(setuptools.__version__)>=parse_version('36.2')

# note: all settings are in settings.ini; edit there, not here
config = ConfigParser(delimiters=['='])
config.read('settings.ini')
cfg = config['DEFAULT']

cfg_keys = 'version description keywords author author_email'.split()
expected = cfg_keys + "lib_name user branch license status min_python audience language".split()
for o in expected: assert o in cfg, "missing expected setting: {}".format(o)
setup_cfg = {o:cfg[o] for o in cfg_keys}

licenses = {
    'apache2': ('Apache Software License 2.0','OSI Approved :: Apache Software License'),
}
statuses = [ '1 - Planning', '2 - Pre-Alpha', '3 - Alpha',
    '4 - Beta', '5 - Production/Stable', '6 - Mature', '7 - Inactive' ]
py_versions = '2.0 2.1 2.2 2.3 2.4 2.5 2.6 2.7 3.0 3.1 3.2 3.3 3.4 3.5 3.6 3.7 3.8'.split()

# requirements = cfg.get('requirements','').split()
lic = licenses[cfg['license']]
min_python = cfg['min_python']

setuptools.setup(
    name = cfg['lib_name'],
    license = lic[0],
    classifiers = [
        'Development Status :: ' + statuses[int(cfg['status'])],
        'Intended Audience :: ' + cfg['audience'].title(),
        'License :: ' + lic[1],
        'Natural Language :: ' + cfg['language'].title(),
    ] + ['Programming Language :: Python :: '+o for o in py_versions[py_versions.index(min_python):]],
    url = cfg['git_url'],
    packages = setuptools.find_packages(),
    include_package_data = True,
    # install_requires = requirements,
    dependency_links = cfg.get('dep_links','').split(),
    python_requires  = '>=' + cfg['min_python'],
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    zip_safe = False,
    entry_points = { 'console_scripts': cfg.get('console_scripts','').split() },
    install_requires = [
        'matplotlib==3.2.2', 'pandas==1.0.5', 'pillow==7.0.0',
        'kornia==0.3.1', 'transformers==2.9.1', 'scikit-learn==0.22.2',
        'fastcore==0.1.17', 'scipy==1.3.1',
    ],
    extras_require={
        'dev': [
            'gdown==3.6.4', 'twine==3.1.1',
            'nbdev==0.2.18',
            'torch @ https://download.pytorch.org/whl/cu101/torch-1.5.0%2Bcu101-cp36-cp36m-linux_x86_64.whl',
            # 'fastai2 @ git+https://github.com/fastai/fastai2.git',
        ]
    },
    **setup_cfg)

