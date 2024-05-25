from setuptools import setup, find_packages
with open('requirements.txt') as requirements_file:
    install_requirements = requirements_file.read().splitlines()
setup(
    name="blocks_duo_autonomic_nervous_system",
    version="1.0.0",
    description="poor noob blocks-duo player package",
    author="autonomic_nervous_system",
    packages=find_packages(),
    install_requires=install_requirements,
    entry_points={
        "console_scripts": [
            "A_N_S_noob=ss_player.main:main",
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.8',
    ]
)