class ConfigClass:
    def __init__(self):
        self.corpusPath = 'C:\\Users\\barif\\PycharmProjects\\Search_Engine\\Data\\date=08-07-2020'
        self.savedFileMainFolder = ''
        self.saveFilesWithStem = self.savedFileMainFolder + "/WithStem"
        self.saveFilesWithoutStem = self.savedFileMainFolder + "/WithoutStem"
        self.toStem = False

        print('Project was created successfully..')

    def get__corpusPath(self):
        return self.corpusPath
