from setuptools import find_packages, setup

setup(
    name="reram_server",
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
        "write_to": "reram_puf/version.py"
    },
    entry_points={
        "console_scripts": [
            "reram_server = reram_puf.reram_server.main:main",
            "reram_client = reram_puf.reram_client.main:main"
        ]
    }
)
