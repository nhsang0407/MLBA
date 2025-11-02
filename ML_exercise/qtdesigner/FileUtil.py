import pickle

class FileUtil:
    @staticmethod
    def savemodel(model, filename):
        try:
            pickle.dump(model, open(filename, 'wb'))
            return True
        except Exception as e:
            print("An exception occurred:", e)
            return False

    @staticmethod
    def loadmodel(filename):
        try:
            model = pickle.load(open(filename, 'rb'))
            return model
        except Exception as e:
            print("An exception occurred:", e)
            return None
