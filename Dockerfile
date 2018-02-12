# Dockerfile for binder
FROM sagemath/sagemath:8.0-2

# Inspired from https://mybinder.readthedocs.io/en/latest/dockerfile.html#preparing-your-dockerfile
# Make sure the contents of our repo are in ${HOME}
COPY --chown=sage:sage README.md ${HOME}/
COPY --chown=sage:sage sage ${HOME}/sage/

RUN cd sage && sage -pip install -e .
