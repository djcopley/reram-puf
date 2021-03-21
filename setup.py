from setuptools import find_packages, setup

setup(
    name="reram-server",
    version="1.0.0",
    license="GPLv3",
    packages=find_packages(),
    install_requires=[
        "pyserial",
    ],
    setup_requires=[
        "setuptools_scm"
    ],
    use_scm_version={
        "relative_to": __file__,
        "write_to": "reram-server/version.py"
    },
    entry_points={
        "console_scripts": [
            "reram-server = reram-server.main:main"
        ]
    }
)
