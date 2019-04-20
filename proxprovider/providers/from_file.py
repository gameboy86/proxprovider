from . import ProxProviderModelBase


class FromFile(ProxProviderModelBase):
    """
    Simple provider with reading proxies from file. There must be only one
    proxy for line.
    Required parameters:
        file_path: Path to file
    """
    def proxies(self, file_path):
        with open(file_path, 'r') as f:
            return [line.strip() for line in f.readlines()]
