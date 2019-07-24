from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(name='inventory-allocator',
      version='0.1',
      install_requires=requirements,
      description='The example solution to the inventory allocator problem',
      url='http://github.com/siweiyang/recruiting-exercises/inventory-allocator/src',
      author='Siwei Yang',
      author_email='s8yang@uwaterloo.ca',
      license='MIT',
      entry_points = {
        'console_scripts': ['inventory-allocator=inventoryallocator:allocate'],
      },
      packages=['inventoryallocator'])
