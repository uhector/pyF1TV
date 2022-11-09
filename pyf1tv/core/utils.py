import typing as t


def dict_to_string(dict_: t.Dict[str, t.Any]) -> str:
    return ' '.join([f'{key} {value}' for key, value in dict_.items()]).strip()
