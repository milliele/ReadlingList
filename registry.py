# -*- coding:utf-8 -*-

"""Registry keeping track of all registered pluggable components"""

# Frames
FRAMES = {}

def register_decorator(register):
    """Returns a decorator that register a class or function to a specified
    register

    Parameters
    ----------
    register : dict
        The register to which the class or function is register

    Returns
    -------
    decorator : func
        The decorator
    """
    def decorator(name):
        """Decorator that register a class or a function to a register.

        Parameters
        ----------
        name : str
            The name assigned to the class or function to store in the register
        """
        def _decorator(function):
            register[name] = function
            function.name = name
            return function
        return _decorator
    return decorator


register_frame = register_decorator(FRAMES)
