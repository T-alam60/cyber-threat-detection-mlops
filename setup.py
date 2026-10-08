from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    """
    This function returns the list of required libraries.
    """
    requirements_list = []

    try:
        with open('requrements.txt', 'r') as file:
            lines = file.readlines()

            for line in lines:
                requirement = line.strip()

                if requirement and requirement != '-e .':
                    requirements_list.append(requirement)

    except FileNotFoundError:
        print("requirements.txt file is not found")

    return requirements_list



print(get_requirements())



setup(
   name='cybersecurity',
    version='0.0.1',
    author='Tanjir Alam',
    author_email='tanjira705@gmail.com',
    description='Cybersecurity Machine Learning Project',
    packages=find_packages(),
    install_requires=get_requirements(),
)