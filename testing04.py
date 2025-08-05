
def idNumberFormat(idNumber):

    idNumber = str(idNumber).strip()
    idNumberLength = len(idNumber)
    idElixerPrefix = ['601', '602', '603', '604', '605', '606', '607', '608', '609']
    idFirstCorePrefix = ['F1', 'F2']
    idPhilippineBatteriesIncPrefix = ['1000','5700']
    idRamcarTechnologyIncPrefix = ['4000']
    idEvergreenPrefix = ["6000"]
    idStaMariaPrefix = ['6800']


    if idNumberLength == 7:
        if idNumber.startswith(tuple(idElixerPrefix)):
            return "Elixer"
        else:
            return "Input company manual"
    elif idNumberLength == 8:
        if idNumber.startswith(tuple(idFirstCorePrefix)):
            return "FirstCore"
        elif idNumber.startswith(tuple(idPhilippineBatteriesIncPrefix)):
            return "Philippine Batteries inc"
        elif idNumber.startswith(idRamcarTechnologyIncPrefix):
            return "Ramcar Technology inc"
        elif idNumber.startswith(idEvergreenPrefix):
            return "evergreen"
        elif idNumber.startswith(idStaMariaPrefix):
            return "sta. maria"
        else:
            return "Input company manual"
print(idNumberFormat('10000882'))