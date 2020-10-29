import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="context_manager_patma",
    version="0.0.1",  # don't change version for now, early development
    author="decorator-factory",
    author_email="appendix.y.z@gmail.com",
    description="Pattern matching with context managers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/decorator-factory/context_manager_patma",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "lark",
    ],
    python_requires='>=3.8',
    package_data={
        "": ["*.md", "*.lark", "*.html", "*.css", "*.fnl"]
    }
)
