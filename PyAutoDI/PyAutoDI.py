from importlib import import_module
from glob import glob

from .Container import Container

def get_module_paths(path_pattern):
    return glob(path_pattern, recursive=True)

def load_modules(module_paths):
    return map(import_module, module_paths)

def register_module(module, container):
    if("register" in module):
        module.register(container)
    else:
        print("Module found that is missing a register function")

def load_and_register_modules(path_pattern, container):
    module_paths = get_module_paths(path_pattern)
    modules = load_modules(module_paths)
    
    for module in modules:
        register_module(module, container)
    
    return container

def get_new_container():
    return Container()
