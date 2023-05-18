from django.shortcuts import render
from django.http import HttpResponse
from .forms import Cliente
import json
from django.http.request import QueryDict
from xls2xlsx import XLS2XLSX

def index(request):
    if "GET" == request.method:
        return render(request, 'polls/index.html')

    else:
        error = "Erro ao processar arquivo excel!"
        try:
            excel_file = request.FILES["excel_file"]
            wb = WB().run(excel_file)
            return render(request, 'polls/index.html', {"list_data": wb, "vars": STANDART_VARS})
        except:
            print(error)
            return render(request, 'polls/index.html', {"error": error})

def processa_formulario(request):
    try:
        varmap = VarMap(request.POST)
        json_varmap = varmap.run()
        response = HttpResponse(json_varmap, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename=variable_map.json'
        response['Content-Length'] = len(response.content)

    except Exception:
        raise
    return response 

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

STANDART_VARS = ["boBootOK", "boModoAuto", "boAlimentaPF", "liCntProdParcial", "Diversos__lrProdHora",
                 "liCntProdTotal", "tSopro__InicPreSopro1", "tSopro__InicPreSopro2",
                 "tSopro__InicPreSopro3", "tSopro__InicPreSopro4", "tSopro__InicPreSopro5", "tSopro__PreSopro1",
                 "tSopro__Calc", "tSopro__Alivio", "tSopro__Residencia", "tEstirFundo", "tExpulsa", "diVel_Silo", "tAlimentaPF",
                 "tLubrifica", "stForno__diPERFIL", "stForno__diVALOR_Z1", "stForno__diVALOR_Z1_PERFIL",
                 "stForno__diVALOR_Z2", "stForno__diVALOR_Z2_PERFIL", "stForno__diVALOR_Z3", "stForno__diVALOR_Z3_PERFIL",
                 "stForno__diVALOR_Z4", "stForno__diVALOR_Z4_PERFIL", "stForno__diVALOR_Z5", "stForno__diVALOR_Z5_PERFIL",
                 "stForno__diVALOR_Z6", "stForno__diVALOR_Z6_PERFIL", "stForno__diVALOR_Z7", "stForno__diVALOR_Z7_PERFIL",
                 "stForno__diVALOR_Z8", "stForno__diVALOR_Z8_PERFIL", "stForno__diVALOR_Z9", "stForno__diVALOR_Z9_PERFIL",
                 "stForno__diVALOR_Z11", "stForno__diVALOR_Z11_PERFIL", "stForno__diVALOR_Z12", "stForno__diVALOR_Z19_PERFIL",
                 "stForno__boBOTAO_ZONA1", "stForno__boBOTAO_ZONA2", "stForno__boBOTAO_ZONA3", "stForno__boBOTAO_ZONA4",
                 "stForno__boBOTAO_ZONA5", "stForno__boBOTAO_ZONA6", "stForno__boBOTAO_ZONA7", "stForno__boBOTAO_ZONA8",
                 "stForno__boBOTAO_ZONA9", "stForno__boBOTAO_ZONA11", "stForno__boBOTAO_ZONA12", "stForno__boBOTAO_ZONA13",
                 "stForno__boBOTAO_ZONA14", "stForno__boBOTAO_ZONA15", "stForno__boBOTAO_ZONA16", "stForno__boBOTAO_ZONA17",
                 "stForno__boBOTAO_ZONA18", "stForno__boBOTAO_ZONA19", "diVelCoifa1", "diVelCoifa2",
                 "stForno__diPERFIL", "Analog__TempCoifa1", "Analog__TempCoifa2", "Analog__TempPF",
                 "Analog__PresAlta", "Analog__PresReserv", "Analog__PresBaixa", "lrPos__Prensa_Aberta",
                 "lrPos__Prensa_Fechada", "lrActTorque__PrensaPos", "lrActTorque__PrensaNeg", "AxisStatus__Pren_BarVolt",
                 "lrPos__Regua_NaPrensa", "lrPos__Regua_NoPosic", "lrActTorque__ReguaPos", "lrActTorque__ReguaNeg",
                 "AxisStatus__Regu_BarVolt", "lrPos__Estir_Topo", "lrPos__Estir_Fundo", "lrActTorque__EstiraPos",
                 "lrActTorque__EstiraNeg", "AxisStatus__Esti_BarVolt", "lrPos__Prensa_Aberta", "lrPos__Prensa_Fechada",
                 "lrActTorque__PrensaPos", "lrActTorque__PrensaNeg", "AxisStatus__Pren_BarVolt", "lrPos__Mesa_NoForno",
                 "lrPos__Mesa_NoPosic", "lrActTorque__MesaPos", "lrActTorque__MesaNeg", "AxisStatus__Mesa_BarVolt",
                 "lrActTorque__Forno", "AxisStatus__Forn_BarVolt", "AxisStatus__Forn_CTemp", "AxisStatus__Forn_PTemp",
                 "lrPos__PosicUp_Aberto", "lrPos__PosicUp_Fechado", "lrActTorque__PosiReguUp", "lrActTorque__PosiCambUp",
                 "AxisStatus__PosiUp_BarVolt", "lrPos__PosicDw_Aberto", "lrPos__PosicDw_Fechado", "lrActTorque__PosiReguDw",
                 "lrActTorque__PosiCambDw", "AxisStatus__PosiDw_BarVolt"]

class Variable():

    def __init__(self, var_par):
        self.var_par = var_par
        self.run()

    # replace local to size
    def local_to_size(self, var_par):
        pl = var_par
        for list1 in pl:
            for par in list1:
                if par == "MODBUS TCP/IP (Zero-based Addressing)":
                    list1[1] = "1"
        return pl

    # replace dots to underline of var name
    def replace_dots(self, lista):
        pl = lista
        for list1 in pl:
            if len(list1) < 4:
                pl.remove(list1)
            else:
                if '.' in list1[0]:
                    list1[0] = list1[0].replace(".", "__")
                if '/' in list1[0]:
                    list1[0] = list1[0].replace("/", "__")
        
        return pl

    # split the list for coils and holding_hegisters

    def split_list(self, lista):
        pl = lista
        l1, l2, l3 = list(), list(), list()
        data = dict()
        for list1 in pl:
            if "0x" in list1:
                l1.append(list1)
            else:
                l2.append(list1)

        l3.append(self.list_to_dict(l1))
        l3.append(self.list_to_dict(l2))
        data["coils"] = l3[0]
        data["holding_registers"] = l3[1]

        return json.dumps(data)

    # convert list to dict
    def list_to_dict(self, lista):
        pl = lista
        l = list()
        for e in pl:
            if len(e) < 6:
                continue
            data = dict()
            data['Name'] = e[0]
            data["Size"] = e[1]
            data["DataType"] = e[5]
            data["Address_1"] = int(e[3])
            data["AccessRight"] = e[4]
            data["GlobalDataType"] = e[5]

            if data["DataType"] == "FLOAT":
                data["Address_1"] = int(e[3])+1

            l.append(data)
        return l

    # run all methods and return a Json file
    def run(self):
        self.var_par = self.local_to_size(self.var_par)
        self.var_par = self.replace_dots(self.var_par)
        return self.split_list(self.var_par)
