FROM python:3.8-alpine
LABEL maintainer='christopher.anthony@libertymutual.com'

# Copy application files into container
COPY * /app/

# Install Flask
RUN pip3 install requests

# Have the container expose port 8088
EXPOSE 8088

# Have the app run as a non-root user
USER 1001

CMD python3 /app/pyblog.py
