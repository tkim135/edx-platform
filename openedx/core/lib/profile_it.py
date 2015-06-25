"""
Ease performance profiling
"""
import os
import tempfile


def log():
    try:
        from cProfile import Profile
    except ImportError:
        from profile import Profile

    def inner(function):
        def wrapper(*args, **kwargs):
            file_descriptor, file_path = tempfile.mkstemp(
                suffix='.profile',
                prefix='platform-',
                dir='/tmp',
            )
            os.close(file_descriptor)
            profile = Profile()
            return_value = profile.runcall(function, *args, **kwargs)
            profile.dump_stats(file_path)
            return return_value
        return wrapper
    return inner
