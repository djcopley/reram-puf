from setuptools import find_packages, setup

setup(
    name="server",
    version="1.0.0",
    license="GPLv3",
    packages=find_packages(),
    install_requires=[
        "pyserial",
        "paho"
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
            "server = reram_puf.server.main:main",
            "client = reram_puf.client.main:main"
        ]
    }
)
