from setuptools import setup, find_packages

setup(
    name="exel-automatic",
    version="1.0.0",
    description="Hybrid SQL Assistant - интерактивный ассистент для SQL-аналитики",
    author="SdvSeven",
    author_email="ssdvseven@gmail.com",
    url="https://github.com/SdvSeven/Exel-Automatic",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.5.0",
        "openpyxl>=3.0.0",
        "requests>=2.28.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "exel-automatic=src.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)