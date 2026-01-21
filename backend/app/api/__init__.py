from .system import router as system_router
from .network import router as network_router
from .io import router as io_router
from .docker import router as docker_router
from .auth import router as auth_router

__all__ = ['system', 'network', 'io', 'docker', 'auth']

system = system_router
network = network_router
io = io_router
docker = docker_router
auth = auth_router
