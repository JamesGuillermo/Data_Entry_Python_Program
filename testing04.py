
def idNumberFormat(idNumber):

    idNumber = str(idNumber).strip()
    idNumberLength = len(idNumber)
    idElixerPrefix = ['601', '602', '603', '604', '605', '606', '607', '608', '609']
    idFirstCorePrefix = ['F1', 'F2']

    if idNumberLength == 7:
        if idNumber.startswith(tuple(idElixerPrefix)):
            return "Elixer Company"
    elif idNumberLength == 8:
        if idNumber.startswith(tuple(idFirstCorePrefix)):
            return "First Core"
        
print(idNumberFormat('F2001234'))