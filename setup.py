from setuptools import find_packages, setup

setup(
    name="milvue_sdk",
    version="1.0",
    description="",
    url="https://github.com/milvue/python-client",
    author="Milvue",
    license="Copyright",
    package_data={"milvue_sdk": ["py.typed"]},
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=["pydantic", "pydicom"],
)
