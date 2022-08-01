import pickle, os, copy

class SharedData:

    def __init__(self):
        self.scheduled_commands = []

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
            try:
                initial_variables = self.__dict__

                saved_variables = {}
                with open('data/data.bin', 'rb') as file:
                    saved_variables_bytes = file.read()
                    saved_variables = pickle.loads(saved_variables_bytes)

                for name, value in initial_variables.items():
                    if name not in saved_variables:
                        saved_variables[name] = value

                self.__dict__ = saved_variables
            except:
                pass

    def clear_shared_data(self):
        """Removes data file (if exists) and sets currently opereated data
        to the initial state."""
        if os.path.exists('data/data.bin'):
            os.remove('data/data.bin')
        
        self.__dict__ = {}
        self.__init__()