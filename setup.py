from setuptools import setup, find_packages

VERSION = '0.0.1b3'

print("""

- upload
    - build wheel: python setup.py sdist
    - upload to server: twine upload dist/*

- download
    - Just pip install <package>

""")


if __name__ == '__main__':
    setup(
        name='fastapi-crud-code-generator',
        version=VERSION,
        install_requires=["aiosqlite<=0.17.0","asyncpg<=0.26.0","fastapi<=0.85.1","greenlet<=1.1.3.post0","Jinja2<=3.1.2",
                          "psycopg2<=2.9.4","pydantic<=1.10.2","SQLAlchemy<=1.4.42","StrEnum<=0.4.8", "uvicorn<=0.19.0"],
        python_requires=">=3.7",
        description="FastaAPI's CRUD project generator for SQLALchemy.",
        long_description=open("README.md",'r',encoding="utf-8").read(),
        long_description_content_type="text/markdown",
        author='Luis Lui',
        author_email='luis11235178@gmail.com',
        url='https://github.com/LuisLuii/fastapi-crud-project-generator',
        license="MIT License",
        keywords=["fastapi", "crud", "restful", "routing","SQLAlchemy", "generator", "crudrouter","postgresql","builder"],
        packages=find_packages("src", include="*.jinja2"),
        package_data={
            '': ['*.jinja2'],
            'src.fastapi_quickcrud_codegen.model.template.common': ['*.jinja2'],
        },
        package_dir={'': 'src'},
        setup_requires=["setuptools>=31.6.0"],
        classifiers=[
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python",
            "Topic :: Internet",
            "Topic :: Software Development :: Libraries :: Application Frameworks",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Code Generators",
            "Topic :: Software Development",
            "Typing :: Typed",
            "Development Status :: 5 - Production/Stable",
            "Environment :: Web Environment",
            "Framework :: AsyncIO",
            "Intended Audience :: Developers",
            "Intended Audience :: Information Technology",
            "Intended Audience :: System Administrators",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
            "Topic :: Internet :: WWW/HTTP",
        ],
        include_package_data=True,
    )