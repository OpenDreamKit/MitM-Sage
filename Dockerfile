# Dockerfile for binder
FROM sagemath/sagemath:8.0-2

# Inspired from https://mybinder.readthedocs.io/en/latest/dockerfile.html#preparing-your-dockerfile
# Make sure the contents of our repo are in ${HOME}
COPY README.md ${HOME}/
COPY sage/ ${HOME}/sage

RUN cd sage && sage -pip install --user -e .
