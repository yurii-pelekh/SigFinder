import os

class SigFinder(object):
    def __init__(self, requiredExtensions, signatureFile):
        self.__requiredExtensions = requiredExtensions
        self.__hexValues = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                            'a', 'b', 'c', 'd', 'e', 'f']
        self.__signatureList = self.__generateSignatureList(signatureFile)

    def __generateSignatureList(self, signatureFile):
        signatureList = []
        signatureItem = []

        with open(signatureFile, 'rb') as f:
            while True:
                buffer = f.read(2)
                if not buffer: break

                bufferStr = buffer.decode()
                if 'x' in bufferStr:
                    if len(signatureItem) > 0:
                        signatureList.append(signatureItem.copy())
                        signatureItem.clear()
                    signatureList.append(bufferStr)
                    continue

                signatureItem.append(int(buffer, 16))
        if len(signatureItem) > 0: signatureList.append(signatureItem)
        return signatureList

    def __generateValuesForXsignature(self, valueStr):
        if valueStr[0] == 'x': return self.__formValues(valueStr[1], 1)
        else: return self.__formValues(valueStr[0], 0)

    def __formValues(self, partOfValue, index):
        values =[]
        for val in self.__hexValues:
            if index == 1: hexValue = val + partOfValue
            else: hexValue = partOfValue + val
            values.append(int(hexValue, 16))
        return values

    def __checkSignatureInPiece(self, signatureList, sourceFileContentByteArray):
        startIndex = 0
        endIndex = len(sourceFileContentByteArray)
        counter =0

        for signature in signatureList:
            if type(signature) is str:
                if signature == 'xx':
                    startIndex += 1
                    continue
                else:
                    permissibleValues = self.__generateValuesForXsignature(signature)
                    if int(sourceFileContentByteArray[startIndex]) not in permissibleValues:
                        return False
                    startIndex += 1
                    continue

            if counter > 0: endIndex = startIndex + len(signature)
            signatureBytes = bytes(signature)
            currentIndex = sourceFileContentByteArray.find(signatureBytes, startIndex, endIndex)

            if currentIndex == -1: return False
            startIndex = currentIndex + len(signatureBytes)
            counter += 1

        return True

    def __checkSignatureInWholeData(self, sourceFile, countOfBytes):
        if len(self.__signatureList) == 0: return False

        with open(sourceFile, 'rb') as f:
            sourceFileContent = f.read(countOfBytes)

        contentByteArray = bytearray(sourceFileContent)
        while len(contentByteArray) >= len(self.__signatureList):
            if self.__checkSignatureInPiece(self.__signatureList, contentByteArray):
                return True
            contentByteArray.pop(0)

        return False

    def  searchInFiles(self, srcDir, destDir, bytesCount):
        for dirPath, subDirs, files in os.walk(srcDir):
            for file in files:
                fileNameWithoutExt, extension = os.path.splitext(file)
                if extension not in self.__requiredExtensions:
                    continue

                fullFilePath = os.path.join(dirPath, file)
                if self.__checkSignatureInWholeData(fullFilePath, bytesCount):
                    print("%s matches the signature" % file)
                    os.system("copy %s %s" % (fullFilePath, destDir))