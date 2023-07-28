from setuptools import setup

long_description = ""
with open("README.md", "r") as fh:
    long_description = fh.read()
    # search for any lines that contain <img and remove them
    long_description = long_description.split("\n")
    long_description = [line for line in long_description if not "<img" in line]
    # now join all the lines back together
    long_description = "\n".join(long_description)


setup(
    name="easycompletion",
    version='0.3.0',
    description="Easy text completion and function calling. Also includes useful utilities for counting tokens, composing prompts and trimming them to fit within the token limit.",
    long_description=long_description,  # added this line
    long_description_content_type="text/markdown",  # and this line
    url="https://github.com/AutonomousResearchGroup/easycompletion",
    author="Moon",
    author_email="shawmakesmagic@gmail.com",
    license="MIT",
    packages=["easycompletion"],
    install_requires=["openai", "tiktoken", "python-dotenv", "rich"],
    readme="README.md",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
