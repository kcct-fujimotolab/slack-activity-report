import datetime
import shlex

import dateutil.parser


class NotEnoughArgumentError(Exception):
    pass


class CommandArguments(object):

    def __init__(self):
        self._defined_args = []
        self.typeobj = type

    def define(self, name, optional=False, type=str):
        if not isinstance(type, self.typeobj):
            raise TypeError("invalid type for define(): {}".format(type))

        self._defined_args.append(
            {'name': name, 'optional': optional, 'type': type})

    def parse(self, argv):
        args = _ArgumentsDictionary()
        n_args = len(argv)

        for i, defined_arg in enumerate(self._defined_args):
            # when get the argument
            if n_args > i:
                if defined_arg['type'] in (datetime.datetime, datetime.date, datetime.time):
                    try:
                        dt = dateutil.parser.parse(argv[i])

                        if defined_arg['type'] == datetime.datetime:
                            args[defined_arg['name']] = dt

                        if defined_arg['type'] == datetime.date:
                            args[defined_arg['name']] = dt.date()

                        if defined_arg['type'] == datetime.time:
                            args[defined_arg['name']] = dt.time()

                    except Exception as e:
                        raise ValueError(e)

                else:
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
