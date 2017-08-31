from copy import deepcopy

from .. import variable


class Layerlike(object):
    def get_params(self):
        raise NotImplementedError

    def forward(self, x, is_training):
        raise NotImplementedError


class Layer(Layerlike):
    def __init__(self):
        super().__init__()
        self._params = []

    def add_param(self, arr):
        param = variable(arr)
        self._params.append(param)
        return param

    def get_params(self):
        return self._params


class Spec(object):
    def build(self, in_shape=None, in_dtype=None):
        raise NotImplementedError

    def __call__(self):
        return self


class Sugar(object):
    """
    A spec factory with default arguments.
    """

    def __init__(self, spec_class, default_kwargs=None):
        assert issubclass(spec_class, Spec)
        if default_kwargs is None:
            default_kwargs = {}
        super().__init__()
        self.spec_class = spec_class
        self.default_kwargs = default_kwargs

    def __call__(self, *args, **override_kwargs):
        kwargs = deepcopy(self.default_kwargs)
        kwargs.update(deepcopy(override_kwargs))
        return self.spec_class(*args, **kwargs)