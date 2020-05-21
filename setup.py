import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="netwave-camera",
    version="0.0.2",
    author="Justin Marentette",
    author_email="justinmarentette11@gmail.com",
    description="A Netwave IP camera API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheLogicMaster/Netwave-Camera",
    license="WTFPL",
    keywords=['Netwave', 'Airsonic', 'Camera'],
    packages=setuptools.find_packages(),
        install_requires=[
          'requests',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        "Operating System :: OS Independent",
        'Topic :: Home Automation',
    ],
    entry_points={
        'console_scripts': [
            'netwave = netwave.__main__:main'
        ]
    },
    python_requires='>=3.6',
)