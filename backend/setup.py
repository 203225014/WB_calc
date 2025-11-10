from setuptools import setup

# The package source is this directory (backend/). We expose it as
# the package named 'wb_calculator' so imports like
#   from wb_calculator import models
# work both in Docker and locally after editable install.
setup(
    name="wb_calculator",
    version="0.1.0",
    packages=["wb_calculator"],
    package_dir={"wb_calculator": ""},
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "sqlalchemy",
        "psycopg2-binary",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "python-dotenv",
        "pydantic-settings",
    ],
)