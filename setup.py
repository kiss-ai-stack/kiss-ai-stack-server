from setuptools import setup, find_packages

setup(
    name="kiss-ai-stack-server",
    version="0.1.0-alpha20",
    description="KISS AI Stack's Server stub",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="KISS AI Stack, Lahiru Pathirage",
    license="MIT",
    python_requires='>=3.12',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "fastapi~=0.115.5",
        "uvicorn~=0.32.1",
        "websockets~=14.1",
        "jose~=1.0.0",
        "bcrypt~=4.2.1",
        "tortoise-orm~=0.22.2",
        "PyJWT~=2.10.1",
        "starlette~=0.41.3",
        "kiss-ai-stack-types~=0.1.0a4",
        "kiss_ai_stack_core~=0.1.0a28"
    ],
    keywords=["ai", "agent", "machine-learning", "llm", "document-processing"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    project_urls={
        "Homepage": "https://github.com/kiss-ai-stack",
        "Repository": "https://github.com/kiss-ai-stack",
        "Documentation": "https://github.com/kiss-ai-stack/kiss-ai-stack-core/main/README.md"
    }
)
