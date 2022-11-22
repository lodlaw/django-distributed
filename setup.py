from setuptools import setup
from pathlib import Path

# read the contents README.md
dir = Path(__file__).parent
long_description = (dir / "README.md").read_text()

setup(name='django_distributed',
      version='0.2',
      description='Distributed databases setup in Django',
      url='https://github.com/anhphamduy/django-distributed',
      author='Anh Pham',
      author_email='anh.pham@lodlaw.com',
      license='MIT',
      packages=['django_distributed', 'django_distributed.router'],
      install_requires=[
          'django-crum',
          'django',
      ],
      zip_safe=False,
      long_description=long_description,
      long_description_content_type='text/markdown',
     )
