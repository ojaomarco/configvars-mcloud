from django.shortcuts import render
from django.http import HttpResponse
from .forms import Cliente
import json
from django.http.request import QueryDict
from xls2xlsx import XLS2XLSX

from .utils import VarMap,WB

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

