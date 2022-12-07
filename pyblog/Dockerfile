FROM python:3.8-alpine
LABEL maintainer='christopher.anthony@libertymutual.com'

# Copy application files into container
COPY * /app/

# Install requests
RUN pip3 install requests

# Have the container expose port 8088
EXPOSE 8088

# Have the app run as a non-root user
USER 1001

# Initial command to start script
ENTRYPOINT python3 /app/pyblog.py

# Default command to run with entrypoint
CMD read
