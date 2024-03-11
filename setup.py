from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent

setup(
    name='passwordcrypto',
    version='1.0.dev1',  # Change the version here
    packages=find_packages(),
    install_requires=[
        "cryptography"
    ],
    long_description=(this_directory / "README.md").read_text(),
    long_description_content_type='text/markdown',  # Use the appropriate content type
    classifiers=[
        
    ],
)