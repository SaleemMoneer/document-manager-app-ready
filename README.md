Document Manager App – Docker Ready

This project demonstrates a Python Tkinter application containerized using Docker.

Notes:
- The application uses Tkinter (GUI).
- GUI support inside Docker is enabled via X11 forwarding on Linux.

Build:
docker build -t document-manager .

Run:
docker run -it \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  document-manager

Firebase credentials file (documentmanagerapp.json) must be provided separately.
