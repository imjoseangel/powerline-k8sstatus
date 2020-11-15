from setuptools import setup

setup(
    name='powerline-k8sstatus',
    description='A Powerline segment for showing the status of current Kubernetes context',
    version='0.1.2',
    keywords='powerline k8s kubernetes status prompt',
    license='MIT',
    author='Jose Angel Munoz',
    author_email='josea.munoz@gmail.com',
    url='https://github.com/imjoseangel/powerline-k8sstatus',
    packages=['powerline_k8sstatus'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Terminals',
        'Topic :: Utilities'
    ],
    install_requires=[
        "kubernetes"
    ]
)
