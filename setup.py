from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt') as req:
        content = req.read()
        requirements = content.split('\n')
    return requirements


setup(
    name='deepseek_api',
    version='0.1.5',
    packages=find_packages(),
    install_requires=read_requirements(),
    description='An unofficial Python API wrapper for chat.Deepseek.com',
)