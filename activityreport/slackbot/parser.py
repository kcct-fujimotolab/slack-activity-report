import shlex


class NotEnoughArgumentError(Exception):
    pass


class CommandArguments(object):

    def __init__(self):
        self._defined_args = []

    def define(self, name, optional=False):
        self._defined_args.append({'name': name, 'optional': optional})

    def parse(self, argv):
        args = _ArgumentsDictionary()
        n_args = len(argv)

        for i, defined_arg in enumerate(self._defined_args):
            # when get the argument
            if n_args > i:
                args[defined_arg['name']] = argv[i]

            # when cannot get the optional argument
            elif defined_arg['optional']:
                args[defined_arg['name']] = None

            # when cannot get the required argument
            else:
                raise NotEnoughArgumentError(
                    'require the <{}> argument'.format(defined_arg['name']))

        return args


class _ArgumentsDictionary(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delattr__


def parse_str(string):
    args = shlex.split(string)
    return args[0].lower(), args[1:]
