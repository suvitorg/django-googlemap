from setuptools import setup, find_packages

setup(
    name='django-googlemap',
    version=__import__('googlemap').VERSION,
    description='Google map field, which saves and reset coordinates',
    author='Suvit Org',
    author_email='mail@suvit.ru',
    url='https://github.com/suvitorg/django-googlemap',
    packages=find_packages(exclude=['docs', 'examples', 'tests']),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'License :: Free for non-commercial use',
        'Intended Audience :: Developers',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Environment :: Web Environment',
        'Topic :: Software Development',
        'Topic :: Office/Business',
        'Topic :: Office/Business :: Financial :: Point-Of-Sale',
    ]
)
