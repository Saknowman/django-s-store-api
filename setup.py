import os

import setuptools

readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
with open(readme_file, 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="django-s-store-api",
    version="1.0.0",
    author="Yuki Sakumoto",
    author_email="snowman.sucking@gmail.com",
    description="django-s-store-api is a simple store rest api of django.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/Saknowman/django-s-store-api",
    packages=[
        's_store_api', 's_store_api.fixtures', 's_store_api.migrations',
        's_store_api.permissions', 's_store_api.tests', 's_store_api.tests.tests_feature',
        's_store_api.utils'
    ],
    license="MIT",
    install_requires=["Django>=3.0", "djangorestframework==3.11"],
    classifiers=[
        'Framework :: Django :: 3.0',
        'Programming Language :: Python',
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.7',
)
