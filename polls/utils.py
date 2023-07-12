from xls2xlsx import XLS2XLSX
import json
class WB():

    def run(self, excel_file):
        x2x = XLS2XLSX(excel_file)
        excel_file = x2x.to_xlsx()
        wb = excel_file
        worksheet = wb.worksheets[0]

        excel_data = list()

        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = list()
            if row[1].value == "Local HMI":
                continue

            # datatype
            row[1].value = self.define_type(row[5].value)

            # type
            if row[2].value == '4x':
                row[2].value = 'holding_registers'
            else:
                row[2].value = 'coils'

            for cell in row:
                if len(str(cell.value)) < 1:
                    continue
                row_data.append(str(cell.value))

            excel_data.append(row_data)
        return excel_data

    def define_type(self, type):
        if type == "Undesignated":
            return ("BIT")
        if type == "16-bit Unsigned":
            return ("INT16")
        if type == "32-bit Float":
            return ("FLOAT")
        if type == "64-bit Unsigned":
            return ("STRING")

class VarMap():
    def __init__(self, request):
        self.dict_request = self.request_to_dict(request)

    def request_to_dict(self, request):
        return dict(request)

    def remove_unnused(self):
        payload = self.dict_request
        if 'csrfmiddlewaretoken' in payload: del payload['csrfmiddlewaretoken']
        return payload

    def map_to_json(self, dict1):
        coils_list = list()
        hr_list = list()
        lenght = range(len(dict1['var_name']))
        for idx in lenght:
            data = dict()
            try:  
                if list(dict1['Relacionar'])[idx] == "relacionar":
                    data['Name'] = list(dict1['var_name'])[idx]
                else: 
                    data['Name'] = list(dict1['Relacionar'])[idx]  
                    
                if '.' in data['Name']:
                    data['Name'] = data['Name'].replace('.', "__")
                if '/' in data['Name']:
                    data['Name'] = data['Name'].replace("/", "__")

                data["Size"] = "1"
                data["DataType"] = list(dict1['datatype'])[idx]
                data["Address_1"] = int(list(dict1['address'])[idx])
                data["AccessRight"] = "ReadWrite"
                data["GlobalDataType"] = list(dict1['datatype'])[idx]

                if data["DataType"] == "FLOAT":
                    data["Address_1"] += 1
                
            except: continue   
            if list(dict1['lenght'])[idx] == 'coils': coils_list.append(data)  
            if list(dict1['lenght'])[idx] == 'holding_registers': hr_list.append(data) 
        var_map = dict()
        var_map['coils']=coils_list
        var_map['holding_registers']=hr_list

        return json.dumps(var_map, indent=4)


    def run(self):
        dict1 = self.remove_unnused()
        return self.map_to_json(dict1)
