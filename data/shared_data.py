import pickle, os

class SharedData:

    def __init__(self):
        self.scheduled_commands = []
        self.some_test = []

        # Searches for any saved variables and saves them if any were found
        self.read_from_file()

    def save_to_file(self):
        """Saves the object's data to the file."""
        with open('data/data.bin', 'wb') as file:
            dumped_variables = pickle.dumps(vars(self))
            file.write(dumped_variables)

    def read_from_file(self):
        """
        Reads data from the file and saves it to the object's
        variables, if succeeds."""
        if os.path.exists('data/data.bin'):
            initial_variables = self.__dict__

            saved_variables = {}
            with open('data/data.bin', 'rb') as file:
                saved_variables_bytes = file.read()
                saved_variables = pickle.loads(saved_variables_bytes)

            for name, value in initial_variables.items():
                if name not in saved_variables:
                    saved_variables[name] = value

            self.__dict__ = saved_variables