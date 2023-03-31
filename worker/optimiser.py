import multiprocessing
from functools import wraps

def optimise(processor):
    """
    Optimises a processor function for maximum speed
    """
    @wraps(processor)
    def wrapper(*args, **kwargs):
        """
        Process function wrapper
        """
        task = multiprocessing.Process(task=processor, args=args, kwargs=kwargs)
        task.start()
        print('processor {} has been optimised'.format())
    return wrapper