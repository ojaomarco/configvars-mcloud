from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

s1,s2 = "Tempo.InicioPS1","tSopro__InicPreSopro1"

STANDART_VARS = ["boBootOK","boModoAuto","boAlimentaPF","liCntProdParcial","Diversos__lrProdHora",
                "liCntProdTotal","tSopro__InicPreSopro1","tSopro__InicPreSopro2",
                "tSopro__InicPreSopro3","tSopro__InicPreSopro4","tSopro__InicPreSopro5","tSopro__PreSopro1",
                "tSopro__Calc","tSopro__Alivio","tSopro__Residencia","tEstirFundo","tExpulsa","diVel_Silo","tAlimentaPF",
                "tLubrifica","stForno__diPERFIL","stForno__diVALOR_Z1","stForno__diVALOR_Z1_PERFIL",
                "stForno__diVALOR_Z2","stForno__diVALOR_Z2_PERFIL","stForno__diVALOR_Z3","stForno__diVALOR_Z3_PERFIL",
                "stForno__diVALOR_Z4","stForno__diVALOR_Z4_PERFIL","stForno__diVALOR_Z5","stForno__diVALOR_Z5_PERFIL",
                "stForno__diVALOR_Z6","stForno__diVALOR_Z6_PERFIL","stForno__diVALOR_Z7","stForno__diVALOR_Z7_PERFIL",
                "stForno__diVALOR_Z8","stForno__diVALOR_Z8_PERFIL","stForno__diVALOR_Z9","stForno__diVALOR_Z9_PERFIL",
                "stForno__diVALOR_Z11","stForno__diVALOR_Z11_PERFIL","stForno__diVALOR_Z12","stForno__diVALOR_Z19_PERFIL",
                "stForno__boBOTAO_ZONA1","stForno__boBOTAO_ZONA2","stForno__boBOTAO_ZONA3","stForno__boBOTAO_ZONA4",
                "stForno__boBOTAO_ZONA5","stForno__boBOTAO_ZONA6","stForno__boBOTAO_ZONA7","stForno__boBOTAO_ZONA8",
                "stForno__boBOTAO_ZONA9","stForno__boBOTAO_ZONA11","stForno__boBOTAO_ZONA12","stForno__boBOTAO_ZONA13",
                "stForno__boBOTAO_ZONA14","stForno__boBOTAO_ZONA15","stForno__boBOTAO_ZONA16","stForno__boBOTAO_ZONA17",
                "stForno__boBOTAO_ZONA18","stForno__boBOTAO_ZONA19","diVelCoifa1","diVelCoifa2",
                "stForno__diPERFIL","Analog__TempCoifa1","Analog__TempCoifa2","Analog__TempPF",
                "Analog__PresAlta","Analog__PresReserv","Analog__PresBaixa","lrPos__Prensa_Aberta",
                "lrPos__Prensa_Fechada","lrActTorque__PrensaPos","lrActTorque__PrensaNeg","AxisStatus__Pren_BarVolt",
                "lrPos__Regua_NaPrensa","lrPos__Regua_NoPosic","lrActTorque__ReguaPos","lrActTorque__ReguaNeg",
                "AxisStatus__Regu_BarVolt","lrPos__Estir_Topo","lrPos__Estir_Fundo","lrActTorque__EstiraPos",
                "lrActTorque__EstiraNeg","AxisStatus__Esti_BarVolt","lrPos__Prensa_Aberta","lrPos__Prensa_Fechada",
                "lrActTorque__PrensaPos","lrActTorque__PrensaNeg","AxisStatus__Pren_BarVolt","lrPos__Mesa_NoForno",
                "lrPos__Mesa_NoPosic","lrActTorque__MesaPos","lrActTorque__MesaNeg","AxisStatus__Mesa_BarVolt",
                "lrActTorque__Forno","AxisStatus__Forn_BarVolt","AxisStatus__Forn_CTemp","AxisStatus__Forn_PTemp",
                "lrPos__PosicUp_Aberto","lrPos__PosicUp_Fechado","lrActTorque__PosiReguUp","lrActTorque__PosiCambUp",
                "AxisStatus__PosiUp_BarVolt","lrPos__PosicDw_Aberto","lrPos__PosicDw_Fechado","lrActTorque__PosiReguDw",
                "lrActTorque__PosiCambDw","AxisStatus__PosiDw_BarVolt"]


