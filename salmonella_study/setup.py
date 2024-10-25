from setuptools import setup, find_packages
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
readme_path = os.path.join(os.path.dirname(current_dir), 'README.md')
setup(
    name="salmonella_study",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "tqdm",
        "thefuzz",
        "missingno"
    ],
    author="Qazi Zarif Ul Islam",
    author_email="zayan.qazi.mail@gmail.com",
    description="A study on Salmonella",
    long_description=open(readme_path).read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/salmonella_study",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)

