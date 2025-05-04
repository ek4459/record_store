from setuptools import setup, find_packages

setup(
    name="record_store",
    version="1.0.0",
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=[
        "mysql-connector-python==8.0.33",
        "keyring==24.2.0",
    ],
    entry_points={
        "console_scripts": [
            "record-store=main:main",
            "setup-database=setup_database:main"
        ]
    },
    author="Eric Knief",
    author_email="ek4459@nyu.edu",
    description="A record store management system",
    python_requires=">=3.8",
)
