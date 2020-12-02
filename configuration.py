
class ConfigClass(object):

    corpusPath = None  # 'C:\\Users\\ronen\\PycharmProjects\\Search_Engine\\testData'
    outputPath = None  # 'C:\\Users\\ronen\\PycharmProjects\\Search_Engine\\json_files'
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
        cls.outputPath = output_path

    @classmethod
    def get__toStem(cls):
        return cls.toStem

    @classmethod
    def set__toStem(cls, to_stem):
        cls.toStem = to_stem
