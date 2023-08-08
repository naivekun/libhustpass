import setuptools

setuptools.setup(
    name="libhustpass",
    version="1.0",
    author="naivekun",
    author_email="naivekun@outlook.com",
    description="A login library for pass.hust.edu.cn",
    url="https://github.com/naivekun/libhustpass",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=["pillow", "pytesseract", "pytest-runner", "pycryptodome"],
    tests_require=["pytest"],
    python_requires=">=3.6",
    test_suite="tests"
)