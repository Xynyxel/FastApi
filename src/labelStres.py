def ceklabelstres(labellist):
    label = ["Cemas","Rileks","Tegang","Tenang"]
    result_list = []
    for data in labellist:
        result_list.append(label[data])          
    return result_list


def ceklabelGSR(labellist):
    label = ['2-4','4-6','<2','>6']
    result_list = []
    for data in labellist:
        result_list.append(label[data])
    return result_list

def ceklabelHR(labellist):
    label = ['60-70','70-90','90-100','>100']
    result_list = []
    for data in labellist:
        result_list.append(label[data])
    return result_list

def ceklabelBP(labellist):
    label = ['100/70-110/75','110/75-120/85','120/90-130/110','>130/110']
    result_list = []
    for data in labellist:
        result_list.append(label[data])
    return result_list

def ceklabelSUHU(labellist):
    label = ['33-35','35-36','36-37','<33']
    result_list = []
    for data in labellist:
        result_list.append(label[data])
    return result_list

def ceklabelRESPIRASI(labellist):
    label = ['16-18','19-20','>20']
    result_list = []
    for data in labellist:
        result_list.append(label[data])
    return result_list

