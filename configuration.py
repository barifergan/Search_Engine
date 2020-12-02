
class ConfigClass(object):

    corpusPath = 'C:\\Users\\ronen\\PycharmProjects\\Search_Engine\\testData'
    outputPath = 'C:\\Users\\ronen\\PycharmProjects\\Search_Engine\\json_files'
    savedFileMainFolder = ''
    saveFilesWithStem = savedFileMainFolder + "/WithStem"
    saveFilesWithoutStem = savedFileMainFolder + "/WithoutStem"
    toStem = False

    print('Project was created successfully..')


    @classmethod
    def set__corpusPath(cls, corpus_path):
        cls.corpusPath = corpus_path

    @classmethod
    def get__corpusPath(cls):
        return cls.corpusPath

    @classmethod
    def get__outputPath(cls):
        return cls.outputPath

    @classmethod
    def set__outputPath(cls, output_path):
        cls.outputPathPath = output_path

    @classmethod
    def get__toStem(cls):
        return cls.toStem

    @classmethod
    def set__toStem(cls, to_stem):
        cls.toStem = to_stem


    #
    #
    # def __init__(self):
    #     self.corpusPath = 'C:\\Users\\ronen\\Downloads\\Data'#\\date=07-27-2020'
    #     self.savedFileMainFolder = ''
    #     self.saveFilesWithStem = self.savedFileMainFolder + "/WithStem"
    #     self.saveFilesWithoutStem = self.savedFileMainFolder + "/WithoutStem"
    #     self.toStem = False
    #
    #     print('Project was created successfully..')
    #
    # @staticmethod
    # def get__corpusPath(self):
    #     return self.corpusPath

