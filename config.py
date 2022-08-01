import os, textwrap

# config = {
#     'window_width': 1000,
#     'window_height': 615
# }

class Config:

    def __init__(self):
        # Default settings (if somehow config.txt doesn't exist)
        self.window_width = 1000
        self.window_height = 615
        self.get_config()

    def get_config(self):
        if os.path.exists('config.txt'):
            config_values = self.__dict__
            with open('config.txt', 'r') as config:
                for line in config.readlines():
                    if line[0] != '#' and len(line) > 1:
                        line_formatted = line.replace(' ', '')
                        line_formatted = line_formatted.rstrip('\n')

                        key, value = line_formatted.split('=')

                        if key in config_values:
                            if not isinstance(value, type(config_values[key])):
                                value = __builtins__[
                                    type(config_values[key]).__name__](value)
                                
                        config_values[key] = value
        else:
            raise FileNotFoundError('Config file is missing.')

    def save_config(self):
        with open('config.txt', 'w') as config:
            notes = """
            # Note: anything except values shouldn't be changed, doing that may result in
            # not correct work of the application!
            # Note: playing with wrong types of values may also result in not correct work
            # of the application!\n
            """
            config.write(textwrap.dedent(notes))
            for key, value in self.__dict__.items():
                config.write(f'{key}={value}\n')