# Dockerfile for binder
# References:
# - https://mybinder.readthedocs.io/en/latest/dockerfile.html#preparing-your-dockerfile
# - https://github.com/sagemath/sage-binder-env/blob/master/Dockerfile

# FROM sagemath/sagemath:8.3

# Copy the README and the contents of sage/ the repo in ${HOME}
COPY --chown=sage:sage README.md ${HOME}/
COPY --chown=sage:sage sage ${HOME}/sage/

RUN sage -i database_gap
RUN cd sage && sage -pip install -e . --process-dependency-links --upgrade

# CMD sage sage/demo_sage_scscp_server.py > sage/demo_sage_scscp_server.log 2>&1
