from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='storyscript',
    version='0.0.2',
    description='interpreted language',
    url='https://github.com/storyscriptorg/storyscript',
    author='lines-of-code',
    author_email='EMAIL',
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['storyscript','storyscript_mathparse'],
    install_requires=[
                      'colorama==0.4.4',
                      'numpy==1.21.1',
                      'Pyinstrument'
                      ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
    ],
)
