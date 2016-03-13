# coding: utf-8
import psycopg2

'''
Created on 31/08/2012

@author: Adriano Santos

TODO: Realizar um refectory URGENTE nesta classe. Tudo que foi desenvolvido aqui foi, apenas, para análise da proposta.
'''
from string import lower
'''
Método utilizado normalizar as expressoes no formato
#"from" mes dia, ano "to" mes dia, ano 
Retornando o intervalo no formato : Data < X < Data.
'''

from datetime import datetime, date, timedelta
import re


day_numbers = "(1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31)"
#year = "((?<=\s)\d{4}|^\d{4})"
year = "\d{4}"
month = "(january|february|march|april|may|june|july|august|september|october|november|december)"
mesesNumericos="(01|02|03|04|05|06|07|08|09|1|2|3|4|5|6|7|8|9|10|11|12)"
meses = {'january':'01','february':'02','march':'03','april':'04','may':'05','june':'06','july':'07','august':'08','september':'09','october':'10','november':'11','december':'12'}
mapNumbers = {'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10,'eleven':11,'twelve':12,'thirteen':13,'fourteen':14,'fifteen':15,'sixteen':16,'seventeen':17,'eighteen':18,'nineteen':19,'twenty':20,'twenty-one':21,'twenty-two':22,'twenty-three':23,'twenty-four':24,'twenty-five':25,'twenty-six':26,'twenty-seven':27,'twenty-eight':28,'twenty-nine':29,'thirty':30,'thirty-one':31,'thirty-two':32,'thirty-three':33,'thirty-four':34,'thirty-five':35,'thirty-six':36,'thirty-seven':37,'thirty-eight':38,'thirty-nine':39,'forty':40,'forty-one':41,'forty-two':42,'forty-three':43,'forty-four':44,'forty-five':45,'forty-six':46,'forty-seven':47,'forty-eight':48,'forty-nine':49,'fifty':50,'fifty-one':51,'fifty-two':52,'fifty-three':53,'fifty-four':54,'fifty-five':55,'fifty-six':56,'fifty-seven':57,'fifty-eight':58,'fifty-nine':59,'sixty':60,'sixty-one':61,'sixty-two':62,'sixty-three':63,'sixty-four':64,'sixty-five':65,'sixty-six':66,'sixty-seven':67,'sixty-eight':68,'sixty-nine':69,'seventy':70,'seventy-one':71,'seventy-two':72,'seventy-three':73,'seventy-four':74,'seventy-five':75,'seventy-six':76,'seventy-seven':77,'seventy-eight':78,'seventy-nine':79,'eighty':80,'eighty-one':81,'eighty-two':82,'eighty-three':83,'eighty-four':84,'eighty-five':85,'eighty-six':86,'eighty-seven':87,'eighty-eight':88,'eighty-nine':89,'ninety':90,'ninety-one':91,'ninety-two':92,'ninety-three':93,'ninety-four':94,'ninety-five':95,'ninety-six':96,'ninety-seven':97,'ninety-eight':98,'ninety-nine':99,'a hundred':100,'one hundred':100,'a thousand':1000,'one thousand':1000}
qtdNum = "([0-9]+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|twenty-one|twenty-two|twenty-three|twenty-four|twenty-five|twenty-six|twenty-seven|twenty-eight|twenty-nine|thirty|thirty-one|thirty-two|thirty-three|thirty-four|thirty-five|thirty-six|thirty-seven|thirty-eight|thirty-nine|forty|forty-one|forty-two|forty-three|forty-four|forty-five|forty-six|forty-seven|forty-eight|forty-nine|fifty|fifty-one|fifty-two|fifty-three|fifty-four|fifty-five|fifty-six|fifty-seven|fifty-eight|fifty-nine|sixty|sixty-one|sixty-two|sixty-three|sixty-four|sixty-five|sixty-six|sixty-seven|sixty-eight|sixty-nine|seventy|seventy-one|seventy-two|seventy-three|seventy-four|seventy-five|seventy-six|seventy-seven|seventy-eight|seventy-nine|eighty|eighty-one|eighty-two|eighty-three|eighty-four|eighty-five|eighty-six|eighty-seven|eighty-eight|eighty-nine|ninety|ninety-one|ninety-two|ninety-three|ninety-four|ninety-five|ninety-six|ninety-seven|ninety-eight|ninety-nine|a hundred|one hundred|a thousand|one thousand)" #20140415 - George Alves

#20150505 - George Alves - INICIO 
preposicoes="(weeks from|until|about|nearly|almost|at least|In a|on the|in|on|at|of|since|from|to|by|after|early|between|before|next)"
#20150505 - George Alves - FIM 

#20140505 - George Alves - INICIO 
diaIndefinido = "^\[\?\]-([1-9]|0[1-9]|1[0,1,2])-((\d{4})|(\d{3}))$"
mesIndefinido = "^([1-9]|[1-9]|0[1-9]|[1,2][0-9]|3[0,1])-\[\?\]-((\d{4})|(\d{3}))$"
anoIndefinido = "^([1-9]|[1-9]|0[1-9]|[1,2][0-9]|3[0,1])-([1-9]|0[1-9]|1[0,1,2])-\[\?\]"

__DIA_INDEFINIDO_EX = "^\d{4}-(0[1-9]|1[0,1,2]|"+month+")$"
__MES_INDEFINIDO_EX = "^([1-9]|[1-9]|0[1-9]|[1,2][0-9]|3[0,1])-\[\?\]-\d{4}$"
__ANO_INDEFINIDO_EX = "^([1-9]|0[1-9]|[1,2][0-9]|3[0,1])-([1-9]|0[1-9]|1[0,1,2]|"+month+")$"
__ANO_INDEFINIDO_INV_EX = "^([1-9]|0[1-9]|1[0,1,2]|"+month+")-([1-9]|0[1-9]|[1,2][0-9]|3[0,1])$"

#20140505 - George Alves - FIM

'Lista de Padrões Mapeados para normalização'
__AA_EX = "(" + year + " - " + year + ")" 
__AA_SEM_ESPACO_EX = "(" + year + "-" + year + ")" 
__FromMDAToMDA_EX = "(^from " + month + " " + day_numbers + ", " + year + " to " + month + " " + day_numbers + ", " + year + ")$"
__FromMDToMD_EX = "(^from " + month + " " + day_numbers + " to " + month + " " + day_numbers + ")$" 
__FromMToM_EX = "(^from " + month + " to " + month + ")$"
__MD_MD_EX = "(" + month + " " + day_numbers + " *- *" + month + " " + day_numbers + ")$"
__MDA_EX = "^(" + month + " " + day_numbers + ", *" + year + ")$"
__AfterMDA_EX = "^(after " + month + " " + day_numbers + ", *" + year + ")$"
__BeforeMDA_EX = "^(before " + month + " " + day_numbers + ", *" + year + ")$"
__DMA_EX = "^(" + day_numbers + " " + month + " " + year + ")$" 
__MA_EX = "^(" + month + " " + year + ")$" 
__MD_EX = "^(" + month + " " + day_numbers + ")$" 
# 20140415 - George Alves - INICIO 
__EBT_COMPLETO_INV_EX = "("+year+"-("+mesesNumericos+"|"+month+")-"+day_numbers+")"
__EBT_COMPLETO_EX = "^("+day_numbers+"-("+mesesNumericos+"|"+month+")-"+year+")"
__X_YEARS_BEFORE_EX = "^("+qtdNum+" year[s]* before)$"
__X_YEARS_EARLY_EX  = "^("+qtdNum+" year[s]* early)$"
__X_YEARS_EARLIER_EX  = "^("+qtdNum+" year[s]* earlier)$"
__X_YEARS_LATE_EX   = "^("+qtdNum+" year[s]* late)$"
__X_YEARS_LATER_EX  = "^("+qtdNum+" year[s]* later)$"
__X_YEARS_AFTER_EX  = "^("+qtdNum+" year[s]* after)$"
__AFTER_X_YEARS_EX  = "^(after "+qtdNum+" year[s]*)$"
__BEFORE_X_YEARS_EX = "^(before "+qtdNum+" year[s]*)$"


__EARLY_X_YEARS_EX = "^(early "+qtdNum+" year[s]*)$"



__X_MONTHS_BEFORE_EX = "^("+qtdNum+" month[s]* before)$"
__X_MONTHS_EARLY_EX  = "^("+qtdNum+" month[s]* early)$"
__X_MONTHS_EARLIER_EX  = "^("+qtdNum+" month[s]* earlier)$"
__X_MONTHS_LATE_EX   = "^("+qtdNum+" month[s]* late)$"
__X_MONTHS_LATER_EX  = "^("+qtdNum+" month[s]* later)$"
__X_MONTHS_AFTER_EX  = "^("+qtdNum+" month[s]* after)$"
__AFTER_X_MONTHS_EX  = "^(after "+qtdNum+" month[s]*)$"
__BEFORE_X_MONTHS_EX = "^(before "+qtdNum+" month[s]*)$"

__EARLY_X_MONTHS_EX = "^(early "+qtdNum+" month[s]*)$"


__X_DAYS_BEFORE_EX = "^("+qtdNum+" day[s]* before)$"
__X_DAYS_EARLY_EX  = "^("+qtdNum+" day[s]* early)$"
__X_DAYS_LATE_EX   = "^("+qtdNum+" day[s]* late)$"
__X_DAYS_LATER_EX  = "^("+qtdNum+" day[s]* later)$"
__X_DAYS_AFTER_EX  = "^("+qtdNum+" day[s]* after)$"
__AFTER_X_DAYS_EX  = "^(after "+qtdNum+" day[s]*)$"
__BEFORE_X_DAYS_EX = "^(before "+qtdNum+" day[s]*)$"

__EARLY_X_DAYS_EX = "^(early "+qtdNum+" day[s]*)$"

__ANO_EX= "^("+year+")$"


# George Alves - 20140618 - INICIO
__X_YEARS_BEFORE_EX_DE = "("+qtdNum+" year[s]* before [0-9a-zA-Z]+)"
__X_YEARS_EARLY_EX_DE  = "("+qtdNum+" year[s]* early [0-9a-zA-Z]+)"
__X_YEARS_LATE_EX_DE   = "("+qtdNum+" year[s]* late [0-9a-zA-Z]+)"
__X_YEARS_LATER_EX_DE  = "("+qtdNum+" year[s]* later [a-zA-Z]+)"
__X_YEARS_AFTER_EX_DE  = "("+qtdNum+" year[s]* after [0-9a-zA-Z]+)"
__AFTER_X_YEARS_EX_DE  = "(after "+qtdNum+" year[s]* [0-9a-zA-Z]+)"
__BEFORE_X_YEARS_EX_DE = "(before "+qtdNum+" year[s]* [0-9a-zA-Z]+)"

__X_MONTHS_BEFORE_EX_DE = "("+qtdNum+" month[s]* before [0-9a-zA-Z]+)"
__X_MONTHS_EARLY_EX_DE  = "("+qtdNum+" month[s]* early [0-9a-zA-Z]+)"
__X_MONTHS_LATE_EX_DE   = "("+qtdNum+" month[s]* late [0-9a-zA-Z]+)"
__X_MONTHS_LATER_EX_DE  = "("+qtdNum+" month[s]* later [0-9a-zA-Z]+)"
__X_MONTHS_AFTER_EX_DE  = "("+qtdNum+" month[s]* after [0-9a-zA-Z]+)"
__AFTER_X_MONTHS_EX_DE  = "(after "+qtdNum+" month[s]* [0-9a-zA-Z]+)"
__BEFORE_X_MONTHS_EX_DE = "(before "+qtdNum+" month[s]* [0-9a-zA-Z]+)"

__X_DAYS_BEFORE_EX_DE = "("+qtdNum+" day[s]* before [0-9a-zA-Z]+)"
__X_DAYS_EARLY_EX_DE  = "("+qtdNum+" day[s]* early [0-9a-zA-Z]+)"
__X_DAYS_EARLIER_EX_DE  = "("+qtdNum+" day[s]* earlier [0-9a-zA-Z]+)"
__X_DAYS_LATE_EX_DE   = "("+qtdNum+" day[s]* late [0-9a-zA-Z]+)"
__X_DAYS_LATER_EX_DE  = "("+qtdNum+" day[s]* later [0-9a-zA-Z]+)"
__X_DAYS_AFTER_EX_DE  = "("+qtdNum+" day[s]* after [0-9a-zA-Z]+)"
__AFTER_X_DAYS_EX_DE  = "(after "+qtdNum+" day[s]* [0-9a-zA-Z]+)"
__BEFORE_X_DAYS_EX_DE = "(before "+qtdNum+" day[s]* [0-9a-zA-Z]+)"
__EX_DE = "([a-zA-Z]+)"

__PRE_EMT_ANO = "^("+preposicoes+" "+year+")$"
__PRE_EBT_DIA_MES = "^("+preposicoes+" "+day_numbers+" ("+month+"|"+mesesNumericos+"))$"
__PRE_MES = "^("+preposicoes+" ("+month+"))$"
__MES_EX = "^("+month+")$"

__PRE_EBT_MES_ANO_EX = "("+preposicoes+" ("+month+"|"+mesesNumericos+") of "+year+")"

__PRE_EBT_COMPL_EX = "^("+preposicoes+" "+day_numbers+" "+month+" "+year+")$"

__PRE_EMT_EMT_COMPL_EX = "("+preposicoes+" "+day_numbers+" "+month+"-"+day_numbers+" "+month+" "+year+")"


__PRE_EMT_MES_DIA_EX = "^("+preposicoes+" ("+month+"|"+mesesNumericos+") "+day_numbers+")$"
__PRE_EMT_MES_ANO_EX = "^("+preposicoes+" ("+month+"|"+mesesNumericos+") "+year+")$"
__PRE_EBT_COMPL_2_EX = "^("+preposicoes+" "+month+" "+day_numbers+", "+year+")$"

__DDMM_DD_MM_EX = "^("+day_numbers+") ("+month+")-"+"("+day_numbers+") ("+month+")$"
__EARLY_IN_YYYY_EX = "^eayly in \d{4}$"

__FROM_YYYY_UNTIL_YYYY_EX = "^from \d{4} until \d{4}$"

# George Alves - 20140618 - FIM

__ANO = "ANO"
__MES = "MES"
__DIA = "DIA"
__FLAG_BEFORE = "X"
__FLAG_AFTER = ""

# 20140415 - George Alves - FIM 


# Normalização de valores
def Normalization(text, ruleMatched):
    #Inicia um array com todos os padrões mapeados
    #20140415 - George Alves- Inclusao dos novos padroes - INICIO 
    arrayFromEx = [__PRE_EBT_COMPL_2_EX, __PRE_EMT_MES_DIA_EX, __PRE_EMT_MES_ANO_EX, __PRE_EBT_COMPL_EX, __PRE_EBT_MES_ANO_EX, __PRE_EMT_EMT_COMPL_EX, __PRE_EMT_ANO, __EBT_COMPLETO_EX, __EBT_COMPLETO_INV_EX, __AA_EX, __AA_SEM_ESPACO_EX , __FromMDAToMDA_EX, __FromMDToMD_EX, __FromMToM_EX, __MD_MD_EX, __MDA_EX, __AfterMDA_EX, __BeforeMDA_EX, __DMA_EX, __MA_EX, __MD_EX, __X_YEARS_BEFORE_EX,__X_YEARS_EARLY_EX , __X_YEARS_EARLIER_EX, __X_YEARS_LATE_EX  ,__X_YEARS_LATER_EX ,__X_YEARS_AFTER_EX ,__AFTER_X_YEARS_EX ,__BEFORE_X_YEARS_EX, __X_MONTHS_BEFORE_EX , __X_MONTHS_EARLY_EX, __X_MONTHS_EARLIER_EX  , __X_MONTHS_LATE_EX   , __X_MONTHS_LATER_EX  , __X_MONTHS_AFTER_EX  , __AFTER_X_MONTHS_EX  , __BEFORE_X_MONTHS_EX , __X_DAYS_BEFORE_EX   , __X_DAYS_EARLY_EX    , __X_DAYS_LATE_EX     , __X_DAYS_LATER_EX    , __X_DAYS_AFTER_EX    , __AFTER_X_DAYS_EX    , __BEFORE_X_DAYS_EX, __ANO_EX, __EARLY_X_YEARS_EX, __EARLY_X_DAYS_EX, __EARLY_X_MONTHS_EX, __DDMM_DD_MM_EX, __EARLY_IN_YYYY_EX, __PRE_EBT_DIA_MES, __FROM_YYYY_UNTIL_YYYY_EX] 
    #20140415 - George Alves- Inclusao dos novos padroes - FIM 
    value = None
    maxLen = 0
    maxRegex = ""
    maxList = []
    for regex in arrayFromEx:
        list = __ExpressionReturn(regex, text)
                
        if len(list) > 0:
            # 20150421 - George Alves - INICIO 
            if (regex == __PRE_EBT_COMPL_2_EX or regex == __PRE_EMT_MES_DIA_EX or regex == __PRE_EMT_MES_ANO_EX or regex == __PRE_EBT_COMPL_EX or regex == __EBT_COMPLETO_EX or regex == __EBT_COMPLETO_INV_EX or regex == __AA_SEM_ESPACO_EX or regex == __MD_EX or regex == __ANO_EX or regex == __PRE_EBT_MES_ANO_EX or regex == __DDMM_DD_MM_EX or regex == __EARLY_IN_YYYY_EX or regex == __PRE_EBT_DIA_MES or regex == __FROM_YYYY_UNTIL_YYYY_EX):
                list = [text]
            # 20150421 - George Alves - FIM 
            if len(list[0]) > maxLen:
                maxLen = len(list[0])
                maxRegex = regex
                maxList = list
    if len(maxList) > 0:
        return __NormalizedValue(maxRegex, maxList)
    return 'Variacao do Padrão ' + ruleMatched + ' ainda não foi mapeado'


# 20140617- George Alves - INICIO 
def NormalizationDateInExpression(text, ruleMatched):
    #Inicia um array com todos os padrões mapeados
    #20140415 - George Alves- Inclusao dos novos padroes - INICIO 
    arrayFromEx = [__X_YEARS_BEFORE_EX_DE,__X_YEARS_EARLY_EX_DE ,__X_YEARS_LATE_EX_DE  ,__X_YEARS_LATER_EX_DE ,__X_YEARS_AFTER_EX_DE ,__AFTER_X_YEARS_EX_DE ,__BEFORE_X_YEARS_EX_DE, __X_MONTHS_BEFORE_EX_DE , __X_MONTHS_EARLY_EX_DE  , __X_MONTHS_LATE_EX_DE   , __X_MONTHS_LATER_EX_DE  , __X_MONTHS_AFTER_EX_DE  , __AFTER_X_MONTHS_EX_DE  , __BEFORE_X_MONTHS_EX_DE , __X_DAYS_BEFORE_EX_DE   , __X_DAYS_EARLY_EX_DE, __X_DAYS_EARLIER_EX_DE    , __X_DAYS_LATE_EX_DE     , __X_DAYS_LATER_EX_DE    , __X_DAYS_AFTER_EX_DE    , __AFTER_X_DAYS_EX_DE    , __BEFORE_X_DAYS_EX_DE, __EX_DE] 
    #20140415 - George Alves- Inclusao dos novos padroes - FIM 
    value = None
    maxLen = 0
    maxRegex = ""
    maxList = []
    for regex in arrayFromEx:
        list = __ExpressionReturn(regex, text)        
        if len(list) > 0:
            if (regex == __X_YEARS_AFTER_EX_DE):
                    list = [text]
            if (regex == __EX_DE):
                    list = [text]
            if len(list[0]) > maxLen:
                maxLen = len(list[0])
                maxRegex = regex
                maxList = list
    if len(maxList) > 0:
        return __NormalizedValueEvent(maxRegex, maxList)
    return 'Variacao do Padrão ' + ruleMatched + ' ainda não foi mapeado'
# 20140617- George Alves - FIM 


def NormalizationListAnteriores(text, listNorm,ruleMatched):
    #Inicia um array com todos os padrões mapeados
    #20140415 - George Alves- Inclusao dos novos padroes - INICIO 
    arrayFromEx = [__ANO_INDEFINIDO_EX, __ANO_INDEFINIDO_INV_EX,  __MES_INDEFINIDO_EX, __DIA_INDEFINIDO_EX, __X_YEARS_BEFORE_EX,__X_YEARS_EARLY_EX ,__X_YEARS_EARLIER_EX, __X_YEARS_LATE_EX  ,__X_YEARS_LATER_EX ,__X_YEARS_AFTER_EX ,__AFTER_X_YEARS_EX ,__BEFORE_X_YEARS_EX, __X_MONTHS_BEFORE_EX , __X_MONTHS_EARLY_EX, __X_MONTHS_EARLIER_EX  , __X_MONTHS_LATE_EX   , __X_MONTHS_LATER_EX  , __X_MONTHS_AFTER_EX  , __AFTER_X_MONTHS_EX  , __BEFORE_X_MONTHS_EX , __X_DAYS_BEFORE_EX   , __X_DAYS_EARLY_EX    , __X_DAYS_LATE_EX     , __X_DAYS_LATER_EX    , __X_DAYS_AFTER_EX    , __AFTER_X_DAYS_EX    , __BEFORE_X_DAYS_EX, __PRE_MES, __MES_EX, __EARLY_X_YEARS_EX, __EARLY_X_DAYS_EX, __EARLY_X_MONTHS_EX] 
    #20140415 - George Alves- Inclusao dos novos padroes - FIM 
    
    if (len(listNorm)>0):
        lastNorm = listNorm[len(listNorm)-1]
        auxList = lastNorm.split(" ")
        if (auxList[len(auxList)-1] == "mapeado"):
            return "Padrão anterior não foi mapeado"
        value = None
        for regex in arrayFromEx:
            list = __ExpressionReturn(regex, text)
#            if (len(list) > 0 and regex == __PRE_EBT_DIA_MES):
#                list = [text]
            
            if len(list) > 0:
                return __NormalizedValueListNorm(regex, [text], listNorm)
        return 'Variacao do Padrão ' + ruleMatched + ' ainda não foi mapeado'

    else:
    #20140415 - George Alves- Inclusao dos novos padroes - FIM 
        #20150505 - Normalizacoes que consideram datas anteriores
        arrayFromEx = [__PRE_EBT_DIA_MES, __MES_EX] 
        
        for regex in arrayFromEx:
            list = __ExpressionReturn(regex, text)
            if (len(list) > 0):
                list = [text]
                
            if len(list) > 0:
                return __NormalizedValueListNorm(regex, [text], listNorm)
        
        return "Padrão anterior não foi mapeado"
            
#GAMBIS    
def __NormalizedValue(regex, found):
    if regex == __FromMDAToMDA_EX:
        return __FromMDAToMDA(found)
    elif regex == __FromMDToMD_EX:
        return __FromMDToMD(found)
    elif regex == __FromMToM_EX:
        return __FromMToM(found)
    elif regex == __MD_MD_EX:
        return __MD_MD(found)
    elif regex == __MDA_EX:
        return __MDA(found)
    elif regex == __AfterMDA_EX:
        return __AfterMDA(found)
    elif regex == __BeforeMDA_EX:
        return __BeforeMDA(found)
    elif regex == __DMA_EX:
        return __DMA(found)
    elif regex == __MA_EX:
        return __MA(found)
    elif regex == __MD_EX:
        return __MD(found)
    elif regex == __AA_EX:
        return __AA(found)
    elif regex == __EBT_COMPLETO_EX or regex == __EBT_COMPLETO_INV_EX:
        return __EBT_COMPLETO(found,regex)
    elif regex == __AA_SEM_ESPACO_EX:
        return __AA_SEM_ESPACO(found,regex)
    elif regex == __PRE_EMT_ANO:
        return __PRE_EMT_ANO_NORM(found,regex)
    elif regex == __PRE_EMT_EMT_COMPL_EX:
        return __PRE_EMT_EMT_COMPL_EX_NORM(found,regex)
    elif regex == __ANO_EX:
        return __ANO_NORM(found,regex)
    elif regex == __PRE_EBT_MES_ANO_EX:
        return __PRE_EBT_MES_ANO_EX_NORM(found, regex)
    elif regex == __PRE_EBT_COMPL_EX:
        return __PRE_EBT_COMPL_EX_NORM(found, regex)
    
    elif regex == __PRE_EMT_MES_DIA_EX:
        return __PRE_EMT_MES_DIA_EX_NORM(found, regex)
    elif regex == __PRE_EMT_MES_ANO_EX:
        return __PRE_EMT_MES_ANO_EX_NORM(found, regex)
    elif regex == __PRE_EBT_COMPL_2_EX:
        return __PRE_EBT_COMPL_2_EX_NORM(found, regex)
    
    elif regex == __DDMM_DD_MM_EX:
        return __DDMM_DD_MM_EX_NORM(found, regex)
    elif regex == __EARLY_IN_YYYY_EX:
        return __EARLY_IN_YYYY_EX_NORM(found, regex)
    
    elif regex == __PRE_EBT_DIA_MES:
        return __PRE_EBT_DIA_MES_NORM(found, regex)
    elif regex == __FROM_YYYY_UNTIL_YYYY_EX:
        return __FROM_YYYY_UNTIL_YYYY_EX_NORM(found, regex)
    

#20140416 - George Alves - INICIO 

def __DatasImprecisas (data,qtd,componente,flagBefore):
    
    arrayFromEx = [anoIndefinido, mesIndefinido, diaIndefinido] 
    isMatch = False;
    padraoCasado = "";
    for regex in arrayFromEx:
        expReg = re.compile(regex)
        if expReg.match(data) is not None:
            isMatch = True;
            padraoCasado = regex;
    if isMatch:
        anoAux = 2000;
        mesAux = 1;
        diaAux = 1;
        if mapNumbers.has_key(str(qtd).lower()):
            qtd = mapNumbers.get(str(qtd).lower()); 
        qtd = int(qtd);       
        if componente == "ANO":
            if padraoCasado == anoIndefinido:
                return data;
            elif padraoCasado == mesIndefinido:

                dia = data.split('-')[0]; 
                ano = data.split('-')[2]; 
                
                if mapNumbers.has_key(str(qtd).lower()):
                    qtd = mapNumbers.get(str(qtd).lower());
                qtdCalc  = int(qtd);
                
                if flagBefore == "X":
                    anoFim = int(ano) - qtdCalc;
                else:
                    anoFim = int(ano) + qtdCalc;
                
                return str(dia) + "-[?]-" + str(anoFim);
            else:
                mes = data.split('-')[1]; 
                ano = data.split('-')[2]; 
                
                if mapNumbers.has_key(str(qtd).lower()):
                    qtd = mapNumbers.get(str(qtd).lower());
                qtdCalc  = int(qtd);
                
                if flagBefore == "X":
                    anoFim = int(ano) - qtdCalc;
                else:
                    anoFim = int(ano) + qtdCalc;
                
                return "[?]-"+ str(mes)+"-"+str(anoFim);

        elif componente == "MES":
            qtd = qtd * 30;
            if padraoCasado == anoIndefinido:
                dia = data.split('-')[0]; 
                mes = data.split('-')[1]; 
                
                # dataAux = datetime.date(int(ano), int(mes), int(dia))
                dataAux = date(int(anoAux), int(mes), int(dia))
                
                retorno = "";
                if flagBefore == "X":
                    #retorno = (dataAux - timedelta(days=daysCalc)).strftime('%d-%m') + "-[?]"
                    retorno = ((dataAux - timedelta(days=qtd)).isoformat().split('T')[0]).split('-')[2]+"-"+ ((dataAux - timedelta(days=qtd)).isoformat().split('T')[0]).split('-')[1]+"-[?]"

                else:
                    retorno = ((dataAux + timedelta(days=qtd)).isoformat().split('T')[0]).split('-')[2]+"-"+ ((dataAux + timedelta(days=qtd)).isoformat().split('T')[0]).split('-')[1]+"-[?]"

                return retorno;
            elif padraoCasado == mesIndefinido:
                return data;
            else:
                mes = data.split('-')[1]; 
                ano = data.split('-')[2]; 
                
                
                # dataAux = datetime.date(int(ano), int(mes), int(dia))
                dataAux = date(int(ano), int(mes), int(diaAux))
                
                retorno = "";
                if flagBefore == "X":
                    #retorno = "[?]-" + (dataAux - timedelta(days=daysCalc)).strftime('%m')+"-"+ (dataAux - timedelta(days=daysCalc)).strftime('%Y')
                    retorno = "[?]-" + ((dataAux - timedelta(days=qtd)).isoformat().split('T')[0]).split('-')[1]+"-"+ ((dataAux - timedelta(days=qtd)).isoformat().split('T')[0]).split('-')[0]
                else:
                
                    retorno = "[?]-" + ((dataAux + timedelta(days=qtd)).isoformat().split('T')[0]).split('-')[1]+"-"+ ((dataAux + timedelta(days=qtd)).isoformat().split('T')[0]).split('-')[0]

                return retorno;
                
        elif componente == "DIA":
            if padraoCasado == anoIndefinido:
                dia = data.split('-')[0]; 
                mes = data.split('-')[1]; 
                
                if mapNumbers.has_key(str(qtd).lower()):
                    qtd = mapNumbers.get(str(qtd).lower());
                daysCalc  = int(qtd);
                
                
                # dataAux = datetime.date(int(ano), int(mes), int(dia))
                dataAux = date(int(anoAux), int(mes), int(dia))
                
                retorno = "";
                if flagBefore == "X":
                    #retorno = (dataAux - timedelta(days=daysCalc)).strftime('%d-%m') + "-[?]"
                    retorno = ((dataAux - timedelta(days=daysCalc)).isoformat().split('T')[0]).split('-')[2]+"-"+ ((dataAux - timedelta(days=daysCalc)).isoformat().split('T')[0]).split('-')[1]+"-[?]"

                else:
                    retorno = ((dataAux + timedelta(days=daysCalc)).isoformat().split('T')[0]).split('-')[2]+"-"+ ((dataAux + timedelta(days=daysCalc)).isoformat().split('T')[0]).split('-')[1]+"-[?]"

                return retorno;
            elif padraoCasado == mesIndefinido:
                dia = data.split('-')[0]; 
                ano = data.split('-')[2]; 
                
                if mapNumbers.has_key(str(qtd).lower()):
                    qtd = mapNumbers.get(str(qtd).lower());
                daysCalc  = int(qtd);
                
                
                # dataAux = datetime.date(int(ano), int(mes), int(dia))
                dataAux = date(int(ano), int(mesAux), int(dia))
                
                retorno = "";
                if flagBefore == "X":
                    #retorno = (dataAux - timedelta(days=daysCalc)).strftime('%d') + "-[?]-" + (dataAux - timedelta(days=daysCalc)).strftime('%Y')
                    retorno = ((dataAux - timedelta(days=daysCalc)).isoformat().split('T')[0]).split('-')[2]+"-[?]-"+ ((dataAux - timedelta(days=daysCalc)).isoformat().split('T')[0]).split('-')[0]
                else:
                    retorno = ((dataAux + timedelta(days=daysCalc)).isoformat().split('T')[0]).split('-')[2]+"-[?]-"+ ((dataAux + timedelta(days=daysCalc)).isoformat().split('T')[0]).split('-')[0]

                return retorno;
            else:
                mes = data.split('-')[1]; 
                ano = data.split('-')[2]; 
                if flagBefore == "X":
                    qtd = qtd * -1;
                    
                dataAux = date(int(ano), int(mes), int(diaAux))
                retorno = "[?]-" + ((dataAux + timedelta(days=qtd)).isoformat().split('T')[0]).split('-')[1]+"-"+ ((dataAux + timedelta(days=qtd)).isoformat().split('T')[0]).split('-')[0];
                return retorno;                
    else:
        return None;
        
        
def __NormalizedValueListNorm(regex, found, listNorm):
    if regex == __X_YEARS_BEFORE_EX:
        return __X_YEARS_BEFORE(found,listNorm)
    elif regex == __X_YEARS_EARLY_EX:
        return __X_YEARS_EARLY(found,listNorm)
    elif regex == __X_YEARS_EARLIER_EX:
        return __X_YEARS_EARLY(found,listNorm)
    elif regex == __X_YEARS_LATE_EX:
        return __X_YEARS_LATE(found,listNorm)
    elif regex == __X_YEARS_LATER_EX:
        return __X_YEARS_LATER(found,listNorm)
    elif regex == __X_YEARS_AFTER_EX:
        return __X_YEARS_AFTER(found,listNorm)
    elif regex == __AFTER_X_YEARS_EX:
        return __AFTER_X_YEARS(found,listNorm)
    elif regex == __BEFORE_X_YEARS_EX:
        return __BEFORE_X_YEARS(found,listNorm)
    
    elif regex == __EARLY_X_YEARS_EX:
        return __BEFORE_X_YEARS(found,listNorm)


    elif regex == __X_MONTHS_BEFORE_EX:
        return __X_MONTHS_BEFORE(found,listNorm)
    elif regex == __X_MONTHS_EARLY_EX:
        return __X_MONTHS_EARLY(found,listNorm)
    elif regex == __X_MONTHS_EARLIER_EX:
        return __X_MONTHS_EARLY(found,listNorm)
    elif regex == __X_MONTHS_LATE_EX:
        return __X_MONTHS_LATE(found,listNorm)
    elif regex == __X_MONTHS_LATER_EX:
        return __X_MONTHS_LATER(found,listNorm)
    elif regex == __X_MONTHS_AFTER_EX:
        return __X_MONTHS_AFTER(found,listNorm)
    elif regex == __AFTER_X_MONTHS_EX:
        return __AFTER_X_MONTHS(found,listNorm)
    elif regex == __BEFORE_X_MONTHS_EX:
        return __BEFORE_X_MONTHS(found,listNorm)

    elif regex == __EARLY_X_MONTHS_EX:
        return __BEFORE_X_MONTHS(found,listNorm)


    elif regex == __X_DAYS_BEFORE_EX:
        return __X_DAYS_BEFORE(found,listNorm)
    elif regex == __X_DAYS_EARLY_EX:
        return __X_DAYS_EARLY(found,listNorm)
    elif regex == __X_DAYS_LATE_EX:
        return __X_DAYS_LATE(found,listNorm)
    elif regex == __X_DAYS_LATER_EX:
        return __X_DAYS_LATER(found,listNorm)
    elif regex == __X_DAYS_AFTER_EX:
        return __X_DAYS_AFTER(found,listNorm)
    elif regex == __AFTER_X_DAYS_EX:
        return __AFTER_X_DAYS(found,listNorm)
    elif regex == __BEFORE_X_DAYS_EX:
        return __BEFORE_X_DAYS(found,listNorm)

    elif regex == __EARLY_X_MONTHS_EX:
        return __BEFORE_X_DAYS(found,listNorm)

    
    elif regex == __ANO_INDEFINIDO_EX or regex == __ANO_INDEFINIDO_INV_EX or regex == __MES_INDEFINIDO_EX or regex == __DIA_INDEFINIDO_EX:
        return __EBT_GET_DATA(found,listNorm, regex)

    elif regex == __PRE_MES:
        return __PRE_MES_NORM(found, listNorm, regex)
    
    elif regex == __MES_EX:
        return __MES_NORM(found, listNorm, regex)
#20140416 - George Alves - FIM 


#20140619 - George Alves - INICIO
def __NormalizedValueEvent(regex, found):
    if regex == __X_YEARS_BEFORE_EX_DE or regex == __X_YEARS_EARLY_EX_DE :
        return __X_YEARS_BEFORE_DE(found)
    elif regex == __X_YEARS_LATE_EX_DE or regex == __X_YEARS_LATER_EX_DE or regex == __X_YEARS_AFTER_EX_DE:  
        return __X_YEARS_LATER_DE(found)
    elif regex == __AFTER_X_YEARS_EX_DE:
        return __AFTER_X_YEARS_DE(found)
    elif regex == __BEFORE_X_YEARS_EX_DE:
        return __BEFORE_X_YEARS_DE(found)
    
    elif regex == __EX_DE:
        return __DE(found)

    
    elif regex == __X_MONTHS_BEFORE_EX_DE or regex == __X_MONTHS_EARLY_EX_DE:
        return __X_MONTHS_BEFORE_DE(found)
    elif regex == __X_MONTHS_LATE_EX_DE or regex == __X_MONTHS_LATER_EX_DE or regex == __X_MONTHS_AFTER_EX_DE:
        return __X_MONTHS_LATER_DE(found)
    elif regex == __AFTER_X_MONTHS_EX_DE:
        return __AFTER_X_MONTHS_DE(found)
    elif regex == __BEFORE_X_MONTHS_EX_DE:
        return __BEFORE_X_MONTHS_DE(found)


    elif regex == __X_DAYS_BEFORE_EX_DE or regex == __X_DAYS_EARLY_EX_DE:
        return __X_DAYS_BEFORE_DE(found)
    elif regex == __X_DAYS_LATE_EX_DE or regex == __X_DAYS_LATER_EX_DE or regex == __X_DAYS_AFTER_EX_DE:
        return __X_DAYS_LATER_DE(found)
    elif regex == __AFTER_X_DAYS_EX_DE:
        return __AFTER_X_DAYS_DE(found)
    elif regex == __BEFORE_X_DAYS_EX_DE:
        return __BEFORE_X_DAYS_DE(found)

#TODO - George Alves - INICIO 
def __GET_DATE_EVENT (event):
    saida = ""
    try:
        conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='postgres'")
        cur = conn.cursor()
        cur.execute("""  SELECT de.* from dataentidades de,entidadesnomesalt ena  where upper(ena.nomealt) = upper('"""+event+"""') and upper(ena.nome_entidade) = upper(de.nome_entidade) """)
        rows = cur.fetchall()
        
        saida = ""
        for row in rows:
            saida = row[1]
    except:
        print "I am unable to connect to the database"    
    
    return saida
def __GET_EVENT_ADV_DE (phrase):
    campos = phrase.split(' ')
    count = 0
    retorno = ""
    for campo in campos:
        count = count + 1
        if (count > 3):
            retorno = retorno + campo + " "

    tamanho = len(retorno)-1
    return retorno[:tamanho]
#TODO - George Alves - FIM 

def __X_YEARS_BEFORE_DE(foundList):
    for found in foundList:
        event = __GET_EVENT_ADV_DE(found)
        dataRef = __GET_DATE_EVENT (event)
        campos = found.split(' ');
        years  = campos[0];
        
        if (dataRef.find(' < X < ') != -1):
            datas = dataRef.split(' < X < ');
            data1 = datas[0];
            
            data1Fim = __DataNormalizada(data1, years, __ANO, __FLAG_BEFORE)
            return data1Fim;
        elif (dataRef[:4] == 'X < ' ):
            data =  dataRef.replace('X < ','');
            
            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_BEFORE)
            
            return 'X < '  + dataFim;
        elif (dataRef[:4] == 'X > ' ):
            data =  dataRef.replace('X > ','');
            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_BEFORE)
            return 'X > '  + dataFim;
    
        else:
            data =  dataRef;
    
            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_BEFORE)
            
            return dataFim;

def __X_YEARS_LATER_DE(foundList):
    for found in foundList:
        event = __GET_EVENT_ADV_DE(found)
        dataRef = __GET_DATE_EVENT (event)

        campos = found.split(' ');
        years  = campos[0];
        
        if (dataRef.find(' < X < ') != -1):
            datas = dataRef.split(' < X < ');
            data1 = datas[0];
            
            data1Fim = __DataNormalizada(data1, years, __ANO, __FLAG_AFTER)
            return data1Fim;
        elif (dataRef[:4] == 'X < ' ):
            data =  dataRef.replace('X < ','');
            
            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_AFTER)
            
            return 'X < '  + dataFim;
        elif (dataRef[:4] == 'X > ' ):
            data =  dataRef.replace('X > ','');
            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_AFTER)
            return 'X > '  + dataFim;
    
        else:
            data =  dataRef;
    
            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_AFTER)
            
            return dataFim;
def __AFTER_X_YEARS_DE(foundList):
    for found in foundList:
        event = __GET_EVENT_ADV_DE(found)
        dataRef = __GET_DATE_EVENT (event)
        campos = found.split(' ');
        years  = campos[1];
        
        if (dataRef.find(' < X < ') != -1):
            datas = dataRef.split(' < X < ');
            data1 = datas[0];
            
            data1Fim = __DataNormalizada(data1, years, __ANO, __FLAG_AFTER)
            return data1Fim;
        elif (dataRef[:4] == 'X < ' ):
            data =  dataRef.replace('X < ','');
            
            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_AFTER)
            
            return 'X < '  + dataFim;
        elif (dataRef[:4] == 'X > ' ):
            data =  dataRef.replace('X > ','');
            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_AFTER)
            return 'X > '  + dataFim;
    
        else:
            data =  dataRef;
            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_AFTER)
            
            return dataFim;
        
def __DE(foundList):
    for found in foundList:
        dataRef = __GET_DATE_EVENT (found)

        return dataRef;
        
def __BEFORE_X_YEARS_DE(foundList):
    for found in foundList:
        event = __GET_EVENT_ADV_DE(found)
        dataRef = __GET_DATE_EVENT (event)
        campos = found.split(' ');
        years  = campos[1];
        
        if (dataRef.find(' < X < ') != -1):
            datas = dataRef.split(' < X < ');
            data1 = datas[0];
            
            data1Fim = __DataNormalizada(data1, years, __ANO, __FLAG_BEFORE)
            return data1Fim;
        elif (dataRef[:4] == 'X < ' ):
            data =  dataRef.replace('X < ','');
            
            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_BEFORE)
            
            return 'X < '  + dataFim;
        elif (dataRef[:4] == 'X > ' ):
            data =  dataRef.replace('X > ','');
            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_BEFORE)
            return 'X > '  + dataFim;
    
        else:
            data =  dataRef;
            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_BEFORE)
            
            return dataFim;


def __X_MONTHS_BEFORE_DE(foundList):
    for found in foundList:
    
        event = __GET_EVENT_ADV_DE(found)
        dataRef = __GET_DATE_EVENT (event)
        campos = found.split(' ');
        monthsCalc  = campos[0];

        if (dataRef.find(' < X < ') != -1):
            datas = dataRef.split(' < X < ');
            data1 = datas[0];
            
            retorno1 = __DataNormalizada(data1, monthsCalc, __MES, __FLAG_BEFORE)
                
            return retorno1;
    
        elif (dataRef[:4] == 'X < ' ):
            data =  dataRef.replace('X < ','');
    
            data = datas[0];
            
            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_BEFORE)
            return 'X < '  + retorno;
        elif (dataRef[:4] == 'X > ' ):
            data =  dataRef.replace('X > ','');
    
            data = datas[0];

            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_BEFORE)

            return 'X > '  + retorno;
    
        else:
            data =  dataRef;
            
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());

            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_BEFORE)

            return retorno;
def __X_MONTHS_LATER_DE(foundList):
    for found in foundList:
    
        event = __GET_EVENT_ADV_DE(found)
        dataRef = __GET_DATE_EVENT (event)
        campos = found.split(' ');
        monthsCalc  = campos[0];

        if (dataRef.find(' < X < ') != -1):
            datas = dataRef.split(' < X < ');
            data1 = datas[0];
            
            retorno1 = __DataNormalizada(data1, monthsCalc, __MES, __FLAG_AFTER)
                
            return retorno1;
    
        elif (dataRef[:4] == 'X < ' ):
            data =  dataRef.replace('X < ','');
    
            data = datas[0];
            
            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_AFTER)
            return 'X < '  + retorno;
        elif (dataRef[:4] == 'X > ' ):
            data =  dataRef.replace('X > ','');
    
            data = datas[0];

            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_AFTER)

            return 'X > '  + retorno;
    
        else:
            data =  dataRef;
            
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());

            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_AFTER)

            return retorno;
def __AFTER_X_MONTHS_DE(foundList):
    for found in foundList:
    
        event = __GET_EVENT_ADV_DE(found)
        dataRef = __GET_DATE_EVENT (event)
        campos = found.split(' ');
        monthsCalc  = campos[1];

        if (dataRef.find(' < X < ') != -1):
            datas = dataRef.split(' < X < ');
            data1 = datas[0];
            
            retorno1 = __DataNormalizada(data1, monthsCalc, __MES, __FLAG_AFTER)
                
            return retorno1;
    
        elif (dataRef[:4] == 'X < ' ):
            data =  dataRef.replace('X < ','');
    
            data = datas[0];
            
            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_AFTER)
            return 'X < '  + retorno;
        elif (dataRef[:4] == 'X > ' ):
            data =  dataRef.replace('X > ','');
    
            data = datas[0];

            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_AFTER)

            return 'X > '  + retorno;
    
        else:
            data =  dataRef;
            
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());

            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_AFTER)

            return retorno;
def __BEFORE_X_MONTHS_DE(foundList):
    for found in foundList:
    
        event = __GET_EVENT_ADV_DE(found)
        dataRef = __GET_DATE_EVENT (event)
        campos = found.split(' ');
        monthsCalc  = campos[1];

        if (dataRef.find(' < X < ') != -1):
            datas = dataRef.split(' < X < ');
            data1 = datas[0];
            
            retorno1 = __DataNormalizada(data1, monthsCalc, __MES, __FLAG_BEFORE)
                
            return retorno1;
    
        elif (dataRef[:4] == 'X < ' ):
            data =  dataRef.replace('X < ','');
    
            data = datas[0];
            
            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_BEFORE)
            return 'X < '  + retorno;
        elif (dataRef[:4] == 'X > ' ):
            data =  dataRef.replace('X > ','');
    
            data = datas[0];

            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_BEFORE)

            return 'X > '  + retorno;
    
        else:
            data =  dataRef;
            
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());

            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_BEFORE)

            return retorno;

def __X_DAYS_BEFORE_DE(foundList):
    for found in foundList:
    
        event = __GET_EVENT_ADV_DE(found)
        dataRef = __GET_DATE_EVENT (event)

        campos = found.split(' ');
        daysCalc  = campos[0];

        if (dataRef.find(' < X < ') != -1):
            datas = dataRef.split(' < X < ');
            data1 = datas[0];
            
            retorno1 = __DataNormalizada(data1, daysCalc, __DIA, __FLAG_BEFORE)
            return retorno1;
    
        elif (dataRef[:4] == 'X < ' ):
            data =  dataRef.replace('X < ','');
    
            data = datas[0];
            
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_BEFORE)

            return 'X < '  + retorno;
        elif (dataRef[:4] == 'X > ' ):
            data =  dataRef.replace('X > ','');
    
            data = datas[0];
            
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_BEFORE)

            return 'X > '  + retorno;
    
        else:
            data =  dataRef;
            
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_BEFORE)

            return retorno;
def __X_DAYS_LATER_DE(foundList):
    for found in foundList:
    
        event = __GET_EVENT_ADV_DE(found)
        dataRef = __GET_DATE_EVENT (event)

        campos = found.split(' ');
        daysCalc  = campos[0];

        if (dataRef.find(' < X < ') != -1):
            datas = dataRef.split(' < X < ');
            data1 = datas[0];
            
            retorno1 = __DataNormalizada(data1, daysCalc, __DIA, __FLAG_AFTER)
            return retorno1;
    
        elif (dataRef[:4] == 'X < ' ):
            data =  dataRef.replace('X < ','');
    
            data = datas[0];
            
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_AFTER)

            return 'X < '  + retorno;
        elif (dataRef[:4] == 'X > ' ):
            data =  dataRef.replace('X > ','');
    
            data = datas[0];
            
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_AFTER)

            return 'X > '  + retorno;
    
        else:
            data =  dataRef;
            
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_AFTER)

            return retorno;
def __AFTER_X_DAYS_DE(foundList):
    for found in foundList:
    
        event = __GET_EVENT_ADV_DE(found)
        dataRef = __GET_DATE_EVENT (event)

        campos = found.split(' ');
        daysCalc  = campos[1];

        if (dataRef.find(' < X < ') != -1):
            datas = dataRef.split(' < X < ');
            data1 = datas[0];
            
            retorno1 = __DataNormalizada(data1, daysCalc, __DIA, __FLAG_AFTER)
            return retorno1;
    
        elif (dataRef[:4] == 'X < ' ):
            data =  dataRef.replace('X < ','');
    
            data = datas[0];
            
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_AFTER)

            return 'X < '  + retorno;
        elif (dataRef[:4] == 'X > ' ):
            data =  dataRef.replace('X > ','');
    
            data = datas[0];
            
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_AFTER)

            return 'X > '  + retorno;
    
        else:
            data =  dataRef;
            
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_AFTER)

            return retorno;
def __BEFORE_X_DAYS_DE(foundList):
    for found in foundList:
    
        event = __GET_EVENT_ADV_DE(found)
        dataRef = __GET_DATE_EVENT (event)

        campos = found.split(' ');
        daysCalc  = campos[1];

        if (dataRef.find(' < X < ') != -1):
            datas = dataRef.split(' < X < ');
            data1 = datas[0];
            
            retorno1 = __DataNormalizada(data1, daysCalc, __DIA, __FLAG_BEFORE)
            return retorno1;
    
        elif (dataRef[:4] == 'X < ' ):
            data =  dataRef.replace('X < ','');
    
            data = datas[0];
            
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_BEFORE)

            return 'X < '  + retorno;
        elif (dataRef[:4] == 'X > ' ):
            data =  dataRef.replace('X > ','');
    
            data = datas[0];
            
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_BEFORE)

            return 'X > '  + retorno;
    
        else:
            data =  dataRef;
            
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_BEFORE)

            return retorno;

#20140619 - George Alves - FIM
#20140416 - George Alves - FIM 
    
def __FromMDAToMDA(found):
    for risotime in found:
        risotime = risotime.replace('from ', '')
        datas = risotime.split(' to ');
        dt1=datetime.strptime(datas[0], '%B %d, %Y')
        dt2=datetime.strptime(datas[1], '%B %d, %Y')
        a= dt1.isoformat().split('T')[0]
        b= dt2.isoformat().split('T')[0]
        return a + ' < X < ' + b

#"from" mes dia "to" mes dia : Data < X < Data -- Pegar ano corrente
def __FromMDToMD(found):
    hoje = datetime.today()
    ano = str(hoje.year)
    for risotime in found:
        risotime = risotime.replace('from ', '')
        datas = risotime.split(' to ');
        datas[0] = datas[0] + ano
        datas[1] = datas[1] + ano
        dt1=datetime.strptime(datas[0], '%B %d, %Y')
        dt2=datetime.strptime(datas[1], '%B %d, %Y')
        # a= dt1.strftime('%d-%m-%Y')
        a = (dt1.isoformat().split('T')[0]).split('-')[2]+"-"+ (dt1.isoformat().split('T')[0]).split('-')[1]+"-"+(dt1.isoformat().split('T')[0]).split('-')[0]

        # b= dt2.strftime('%d-%m-%Y')
        b = (dt2.isoformat().split('T')[0]).split('-')[2]+"-"+ (dt2.isoformat().split('T')[0]).split('-')[1]+"-"+(dt2.isoformat().split('T')[0]).split('-')[0]
        return a + ' < X < ' + b

# Expressões para o padrão mes ano
def __MA(found):
    for risotime in found:
        datas = risotime.split(' ')
        return '[?]-' + meses[datas[0].lower()] + '-' + datas[1]

# Expressões para o padrão mes dia
def __MD(found):
    for risotime in found:
        datas = risotime.split(' ')
        #20150424 - George Alves - INICIO 
        if (len(datas) > 2):
            if (len(datas)==4):
                if (datas[1].lower() in month):
                    return datas[2].replace(",","") + '-' + meses[datas[1].lower()] + '-' + datas[3]
                elif (datas[2].lower() in month):
                    return datas[1].replace(",","") + '-' + meses[datas[2].lower()] + '-' + datas[3]
                else:
                    return datas[1].replace(",","") + '-' + datas[2] + '-' + datas[3]
            if (len(datas[2]) > 2):
                return '[?]' + '-' + meses[datas[1].lower()] + '-'+datas[2]
            return datas[2] + '-' + meses[datas[1].lower()] + '-[?]'
        #20150424 - George Alves - FIM
        return datas[1] + '-' + meses[datas[0].lower()] + '-[?]' 



#"from" mes "to" mes : Data < X < Data -- Pegar ano corrente    
def __FromMToM(found):
    hoje = datetime.today()
    ano = str(hoje.year)
    for risotime in found:
        risotime = risotime.replace('from ', '')
        datas = risotime.split(' to ');
        a = '[?]-' + meses[datas[0].lower()] + '-' + ano
        b = '[?]-' + meses[datas[1].lower()] + '-' +  ano
        return a + ' < X < ' + b

#mes dia - mes dia OU mes dia-mes dia: Data < X < Data -- Pegar ano corrente
def __MD_MD(found):

    hoje = datetime.today()
    ano = str(hoje.year)
    
    for risotime in found:
        if (risotime.find(' - ') != -1):
            datas = risotime.split(' - ');
        elif (risotime.find('-') != -1):
            datas = risotime.split('-');
      
        datas[0] = datas[0] + ', ' +  ano
        datas[1] = datas[1] + ', ' +  ano
           
        dt1=datetime.strptime(datas[0], '%B %d, %Y')
        dt2=datetime.strptime(datas[1], '%B %d, %Y')
           
        # a= dt1.strftime('%d-%m-%Y')
        a = (dt1.isoformat().split('T')[0]).split('-')[2]+"-"+ (dt1.isoformat().split('T')[0]).split('-')[1]+"-"+(dt1.isoformat().split('T')[0]).split('-')[0]

        # b= dt2.strftime('%d-%m-%Y')
        b = (dt2.isoformat().split('T')[0]).split('-')[2]+"-"+ (dt2.isoformat().split('T')[0]).split('-')[1]+"-"+(dt2.isoformat().split('T')[0]).split('-')[0]

           
        return a + ' < X < ' + b

#Formato convencional de data mes dia, ano
def __MDA(found):
    for risotime in found:
        dt=datetime.strptime(risotime, '%B %d, %Y')
        
        iso = dt.isoformat()

        tokens = iso.strip().split("T")
        
        campos = tokens[0].split("-")
        
        return campos[2] + "-" + campos[1] + "-" + campos[0]
        #return dt.strftime('%d-%m-%Y')

#Para intervalor anterior aa dada encontrada
def __AfterMDA(found):
    for risotime in found:
        risotime = risotime.replace('after ','')
        dt=datetime.strptime(risotime, '%B %d, %Y')
        return 'X > ' + (dt.isoformat().split('T')[0]).split('-')[2]+"-"+ (dt.isoformat().split('T')[0]).split('-')[1]+"-"+(dt.isoformat().split('T')[0]).split('-')[2]

#Para intervalor posterior aa dada encontrada
def __BeforeMDA(found):
    for risotime in found:
        risotime = risotime.replace('before ','')
        dt=datetime.strptime(risotime, '%B %d, %Y')
        return 'X < ' + (dt.isoformat().split('T')[0]).split('-')[2]+"-"+ (dt.isoformat().split('T')[0]).split('-')[1]+"-"+(dt.isoformat().split('T')[0]).split('-')[0]

#Para datas no formato dia mes ano
def __DMA(found):
    for risotime in found:
        dt=datetime.strptime(risotime, '%d %B %Y')
        return (dt.isoformat().split('T')[0]).split('-')[2]+"-"+ (dt.isoformat().split('T')[0]).split('-')[1]+"-"+(dt.isoformat().split('T')[0]).split('-')[0]
    
#Para datas no formato ano - ano OU ano-ano
def __AA(found):
    for risotime in found:
        if (risotime.find(' - ') != -1):
            datas = risotime.split(' - ');
        elif (risotime.find('-') != -1):
            datas = risotime.split('-');
        return datas[0] + ' < X < ' + datas[1]

def __EBT_COMPLETO(found, regex):
    for risotime in found:
        retorno = ""
        if (regex == __EBT_COMPLETO_EX):
            campos = risotime.split("-")
            dia = campos[0]
            mes  = campos[1]
            ano = campos[2]
            
            if (mes not in mesesNumericos):
                mes = mesesNumericos[mes]
                
            retorno = dia +"-"+ mes +"-"+ ano
        elif (regex == __EBT_COMPLETO_INV_EX):
            campos = risotime.split("-")
            dia = campos[2]
            mes  = campos[1]
            ano = campos[0]
            
            if (mes not in mesesNumericos):
                mes = mesesNumericos[mes]
                
            retorno = dia +"-"+ mes +"-"+ ano
             
        return retorno

def __AA_SEM_ESPACO(found, regex):
    for risotime in found:
        campos = risotime.split("-")
        data1 = campos[0]
        data2 = campos[1]
        
        return "[?]-[?]-"+data1+" < X < "+"[?]-[?]-"+data2

def __ANO_NORM(found, regex):
    for risotime in found:
        return "[?]-[?]-"+risotime
    
def __PRE_EBT_MES_ANO_EX_NORM(found, regex):
    for risotime in found:
        
        campos = risotime.split(" ")
        
        mes  = campos[1]
        ano = campos[3]
            
        if (mes not in mesesNumericos):
            mes = meses[mes.lower()]
                
        retorno = "[?]" +"-"+ mes +"-"+ ano
        
        return retorno
    
def __PRE_EBT_COMPL_EX_NORM(found, regex):
    for risotime in found:
        
        campos = risotime.split(" ")
 
        dia = campos[1]       
        mes  = campos[2]
        ano = campos[3]
            
        if (mes not in mesesNumericos):
            mes = meses[mes.lower()]
                
        retorno = dia +"-"+ mes +"-"+ ano
        
        return retorno
    
def __PRE_EMT_MES_DIA_EX_NORM(found, regex):
    for risotime in found:
        
        campos = risotime.split(" ")
 
        dia = campos[2]       
        mes  = campos[1]
            
        if (mes not in mesesNumericos):
            mes = meses[mes.lower()]
                
        retorno = dia +"-"+ mes +"-[?]"
        
        return retorno

def __DDMM_DD_MM_EX_NORM(found, regex):
    for risotime in found:
        
        campos = risotime.split(" ")
 
        dia1 = campos[0]       
        mes1  = campos[1].split("-")[0]
            
        dia2 = campos[1].split("-")[1]
        mes2 = campos[2]
        
        if (mes1 not in mesesNumericos):
            mes1 = meses[mes1.lower()]
                
        if (mes2 not in mesesNumericos):
            mes2 = meses[mes2.lower()]
                
        retorno = dia1 +"-"+ mes1 +"-[?] < X < " + dia2 + "-" + mes2 + "-[?]"
        
        return retorno
def __EARLY_IN_YYYY_EX_NORM(found, regex):
    for risotime in found:
        
        campos = risotime.split(" ")
 
        ano = campos[2]
                        
        retorno = "[?]-[?]-"+ano

        
        return retorno

def __FROM_YYYY_UNTIL_YYYY_EX_NORM(found, regex):
    for risotime in found:
        
        campos = risotime.split(" ")
 
        ano1 = campos[1];
        ano2 = campos[3];
                        
        retorno = "[?]-[?]-"+ano1+" < X < [?]-[?]-"+ano2

        
        return retorno

def __PRE_EMT_MES_ANO_EX_NORM(found, regex):
    for risotime in found:
        
        campos = risotime.split(" ")
 
        ano = campos[2]       
        mes  = campos[1]
            
        if (mes not in mesesNumericos):
            mes = meses[mes.lower()]
                
        retorno = "[?]-"+ mes +"-"+ano
        
        return retorno

def __PRE_EBT_COMPL_2_EX_NORM(found, regex):
    for risotime in found:
        
        campos = risotime.split(" ")
 
        ano = campos[len(campos)-1]       
        mes  = campos[len(campos)-3]
        dia = campos[len(campos)-2].replace(",","")
            
        if (mes not in mesesNumericos):
            mes = meses[mes.lower()]
                
        retorno = dia+"-"+ mes +"-"+ano
        
        return retorno
    
# 20150505 - George Alves - INICIO 
def __PRE_EMT_ANO_NORM(found, regex):
    for risotime in found:
        campos = risotime.split(" ")
        data = campos[len(campos)-1]

        return "[?]-[?]-"+data

# 20150505 - George Alves - INICIO 
def __PRE_EMT_EMT_COMPL_EX_NORM(found, regex):
    for risotime in found:
        campos = risotime.split(" ")
        
        dia1 = campos[1]
        mes1 = meses[(campos[2].split("-"))[0].lower()]
        ano1 = campos[4]
        
        data1 = dia1 + "-" + mes1 + "-"+ano1
        
        dia2 = campos[2].split("-")[1]
        mes2 = meses[(campos[3].split("-"))[0].lower()]
        ano2 = campos[4]
        
        data2 = dia2 + "-" + mes2 + "-"+ano2
        

        return data1 + " < X < "+data2
    
def __PRE_EBT_DIA_MES_NORM(found, regex):
    for risotime in found:
        campos = risotime.split(" ")
        if (campos[len(campos)-1] in mesesNumericos):
            return campos[len(campos)-2] + "-" + campos[len(campos)-1] + "-[?]";
        elif (campos[len(campos)-1].lower() in month):
            return campos[len(campos)-2] + "-" + meses[campos[len(campos)-1].lower()] + "-[?]";
        
#        if (len(listNorm) > 0):
#            ultimaDataNormalizada = listNorm[len(listNorm)-1]
#                    
#            if (ultimaDataNormalizada == ""):
#                if (campos[2] in mesesNumericos):
#                    return campos[1] + "-" + campos[2] + "-[?]";
#                elif (campos[2].lower() in month):
#                    return campos[1] + "-" + meses[campos[2].lower()] + "-[?]";                
#            else:
                
#                if (ultimaDataNormalizada.find(' < X < ') != -1):
#                    if (campos[2] in mesesNumericos):
#                        return campos[1] + "-" + campos[2] + "-[?]";
#                    elif (campos[2].lower() in month):
#                        return campos[1] + "-" + meses[campos[2].lower()] + "-[?]";
                    
#                elif (ultimaDataNormalizada[:4] == 'X < ' ):
#                    if (campos[2] in mesesNumericos):
#                        return campos[1] + "-" + campos[2] + "-[?]";
#                    elif (campos[2].lower() in month):
#                        return campos[1] + "-" + meses[campos[2].lower()] + "-[?]";
#                elif (ultimaDataNormalizada[:4] == 'X > ' ):
#                    if (campos[2] in mesesNumericos):
#                        return campos[1] + "-" + campos[2] + "-[?]";
#                    elif (campos[2].lower() in month):
#                        return campos[1] + "-" + meses[campos[2].lower()] + "-[?]";
#            
#                else:
#                    data =  ultimaDataNormalizada;
#    
#                    camposAux = data.split("-")
##                    print "aquiiiii --> risotime: "+risotime+". data " + data + "."
#                   
#                   if (campos[2] in mesesNumericos):
#                       return campos[1] + "-" + campos[2] + "-" + camposAux[2];
#                   elif (campos[2].lower() in month):
#                       return campos[1] + "-" + meses[campos[2].lower()] + "-" + camposAux[2];
#               
#        else:
                            
#           if (campos[2] in mesesNumericos):
#                return campos[1] + "-" + campos[2] + "-[?]";
#            elif (campos[2].lower() in month):
#                return campos[1] + "-" + meses[campos[2].lower()] + "-[?]";
            
    
# 20150505 - George Alves - FIM 

#20151210 - George Alves - INICIO
def __PRE_MES_NORM(found, listNorm, regex):
    for risotime in found:
        campos = risotime.split(" ")
        if (len(listNorm) > 0):
            ultimaDataNormalizada = listNorm[len(listNorm)-1]
            #20140415 - George Alves- Inclusao dos novos padroes - FIM 
                    
            if (ultimaDataNormalizada == ""):
                if (campos[1] in mesesNumericos):
                    return "[?]-" + campos[1] + "-[?]";
                elif (campos[1].lower() in month):
                    return "[?]-" + meses[campos[1].lower()] + "-[?]";                
            else:
                
                if (ultimaDataNormalizada.find(' < X < ') != -1):
                    if (campos[1] in mesesNumericos):
                        return campos[1] + "-" + campos[2] + "-[?]";
                    elif (campos[1].lower() in month):
                        return "[?]-" + meses[campos[1].lower()] + "-[?]";
                    
                elif (ultimaDataNormalizada[:4] == 'X < ' ):
                    if (campos[1] in mesesNumericos):
                        return "[?]-" + campos[1] + "-[?]";
                    elif (campos[1].lower() in month):
                        return "[?]-" + meses[campos[1].lower()] + "-[?]";
                elif (ultimaDataNormalizada[:4] == 'X > ' ):
                    if (campos[1] in mesesNumericos):
                        return "[?]-" + campos[1] + "-[?]";
                    elif (campos[1].lower() in month):
                        return "[?]-" + meses[campos[1].lower()] + "-[?]";
            
                else:
                    data =  ultimaDataNormalizada;
    
                    camposAux = data.split("-")
                    print "aquiiiii --> risotime: "+risotime+". data " + data + "."
                    
                    if (campos[1] in mesesNumericos):
                        return "[?]-" + campos[1] + "-" + camposAux[2];
                    elif (campos[1].lower() in month):
                        return "[?]-" + meses[campos[1].lower()] + "-" + camposAux[2];
                
        else:
                            
            if (campos[1] in mesesNumericos):
                return "[?]-" + campos[1] + "-[?]";
            elif (campos[2].lower() in month):
                return "[?]-" + meses[campos[1].lower()] + "-[?]";

#20151220 - George Alves - FIM

#20151211 - George - INICIO
def __MES_NORM(found, listNorm, regex):
    for risotime in found:
        campos = risotime.split(" ")
        if (len(listNorm) > 0):
            ultimaDataNormalizada = listNorm[len(listNorm)-1]
            #20140415 - George Alves- Inclusao dos novos padroes - FIM 
                    
            if (ultimaDataNormalizada == ""):
                if (risotime in mesesNumericos):
                    return "[?]-" + risotime + "-[?]";
                elif (risotime.lower() in month):
                    return "[?]-" + meses[risotime.lower()] + "-[?]";                
            else:
                
                if (ultimaDataNormalizada.find(' < X < ') != -1):
                    return "[?]-" + meses[risotime.lower()] + "-[?]";                    
                elif (ultimaDataNormalizada[:4] == 'X < ' ):
                    return "[?]-" + meses[risotime.lower()] + "-[?]";                    
                elif (ultimaDataNormalizada[:4] == 'X > ' ):
                    return "[?]-" + meses[risotime.lower()] + "-[?]";                    
                else:
                    data =  ultimaDataNormalizada;
    
                    camposAux = data.split("-")
                    
                    if (risotime in mesesNumericos):
                        return "[?]-" + risotime + "-" + camposAux[2];
                    elif (risotime.lower() in month):
                        return "[?]-" + meses[risotime.lower()] + "-" + camposAux[2];
                
        else:
                            
            if (risotime in mesesNumericos):
                return "[?]-" + risotime + "-[?]";
            elif (risotime.lower() in month):
                return "[?]-" + meses[risotime.lower()] + "-[?]";


#20151211 - George - FIM

def __DataNormalizada (data,qtd,componente,flagBefore):
    dataFim = "";
    if (data != ""):        
        if __DatasImprecisas(data, qtd, componente, flagBefore) is None:
            dataFim = __DatasPrecisas(data, qtd, componente, flagBefore)
        else:
            dataFim = __DatasImprecisas(data, qtd, componente, flagBefore)
    return dataFim;
    
def __DatasPrecisas (data,qtd,componente,flagBefore):
    if (data.find('[?]') != -1):
        return ""
        
    if componente == "ANO":
        years = qtd
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        if mapNumbers.has_key(str(qtd).lower()):
            years = mapNumbers.get(str(qtd).lower());
        if (flagBefore == __FLAG_BEFORE):
            years = int(years) * -1;
    
        anoSub = int(ano) + int(years);
        dataFim = str(dia) + '-' + str(mes) + '-' + str(anoSub);
                
        return dataFim;

    elif componente == "MES":
        months = qtd;
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
    
        if mapNumbers.has_key(str(qtd).lower()):
            months = mapNumbers.get(str(qtd).lower());
        if (flagBefore == __FLAG_BEFORE):
            months = int(months) * -1;
            
        daysCalc  = int(months) * 30;

    
        dataAux = date(int(ano), int(mes), int(dia))
        # retorno = (dataAux + timedelta(days=int(daysCalc))).strftime('%d-%m-%Y')
        
        retorno = ((dataAux + timedelta(days=int(daysCalc))).isoformat().split('T')[0]).split('-')[2]+"-"+ ((dataAux + timedelta(days=int(daysCalc))).isoformat().split('T')[0]).split('-')[1]+"-"+((dataAux + timedelta(days=int(daysCalc))).isoformat().split('T')[0]).split('-')[0]
        return retorno;
                
    elif componente == "DIA":
        dias = qtd;
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
    
        if mapNumbers.has_key(str(qtd).lower()):
            dias = mapNumbers.get(str(qtd).lower()); 
        if (flagBefore == __FLAG_BEFORE):
            dias = int(dias) * -1;
            
        dataAux = date(int(ano), int(mes), int(dia))
        #retorno = (dataAux + timedelta(days=int(dias))).strftime('%d-%m-%Y')
        retorno = ((dataAux - timedelta(days=int(dias))).isoformat().split('T')[0]).split('-')[2]+"-"+ ((dataAux - timedelta(days=int(dias))).isoformat().split('T')[0]).split('-')[1]+"-"+((dataAux - timedelta(days=int(dias))).isoformat().split('T')[0]).split('-')[0]
        return retorno;
    
#20140416 - George Alves - INICIO
def __X_YEARS_BEFORE    (foundList, listNorm):
    
    for found in foundList:
        
        ultimaDataNormalizada = listNorm[len(listNorm)-1]
        #20140415 - George Alves- Inclusao dos novos padroes - FIM 
                
        if (ultimaDataNormalizada.find(' < X < ') != -1):
            datas = ultimaDataNormalizada.split(' < X < ');
            data1 = datas[0];

            campos = found.split(' ');
            yearsBefore  = campos[0];
            data1Fim = __DataNormalizada(data1, yearsBefore, __ANO, __FLAG_BEFORE)
            return data1Fim;
            
        elif (ultimaDataNormalizada[:4] == 'X < ' ):
            data =  ultimaDataNormalizada.replace('X < ','');
    
            campos = found.split(' ');
            yearsBefore  = campos[0];
            
            dataFim = __DataNormalizada(data, yearsBefore, __ANO, __FLAG_BEFORE)
            
            return 'X < '  + dataFim;
        elif (ultimaDataNormalizada[:4] == 'X > ' ):
            data =  ultimaDataNormalizada.replace('X > ','');
    
            campos = found.split(' ');
            yearsBefore  = campos[0];
            
            dataFim = __DataNormalizada(data, yearsBefore, __ANO, __FLAG_BEFORE)
            
            return 'X > '  + dataFim;
    
        else:
            data =  ultimaDataNormalizada;
    
            campos = found.split(' ');
            yearsBefore  = campos[0];

            dataFim = __DataNormalizada(data, yearsBefore, __ANO, __FLAG_BEFORE)
            
            return dataFim;
                
def __X_YEARS_EARLY     (foundList, listNorm):

    for found in foundList:
        ultimaDataNormalizada = listNorm[len(listNorm)-1]
        if (ultimaDataNormalizada.find(' < X < ') != -1):
            datas = ultimaDataNormalizada.split(' < X < ');
            data1 = datas[0];
            
            campos = found.split(' ');
            yearsBefore  = campos[0];

            data1Fim = __DataNormalizada(data1, yearsBefore, __ANO, __FLAG_BEFORE)

            return data1Fim;
            
        elif (ultimaDataNormalizada[:4] == 'X < ' ):
            data =  ultimaDataNormalizada.replace('X < ','');
    
            campos = found.split(' ');
            yearsBefore  = campos[0];
            dataFim = __DataNormalizada(data, yearsBefore, __ANO, __FLAG_BEFORE)
            
            return 'X < '  + dataFim;
        elif (ultimaDataNormalizada[:4] == 'X > ' ):
            data =  ultimaDataNormalizada.replace('X > ','');
    
            campos = found.split(' ');
            yearsBefore  = campos[0];

            
            dataFim = __DataNormalizada(data, yearsBefore, __ANO, __FLAG_BEFORE)
            
            return 'X > '  + dataFim;
    
        else:
            data =  ultimaDataNormalizada;
    
            campos = found.split(' ');
            yearsBefore  = campos[0];

            dataFim = __DataNormalizada(data, yearsBefore, __ANO, __FLAG_BEFORE)
            
            return dataFim;


def __X_YEARS_LATE      (foundList, listNorm):
    
    for found in foundList:
        ultimaDataNormalizada = listNorm[len(listNorm)-1]
        if (ultimaDataNormalizada.find(' < X < ') != -1):
            datas = ultimaDataNormalizada.split(' < X < ');
            data2 = datas[1];
            
            campos = found.split(' ');
            years  = campos[0];
            data2Fim = __DataNormalizada(data2, years, __ANO, __FLAG_AFTER)
            
            return data2Fim;
            
        elif (ultimaDataNormalizada[:4] == 'X < ' ):
            data =  ultimaDataNormalizada.replace('X < ','');
    
            campos = found.split(' ');
            years  = campos[0];

            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_AFTER)
            
            return 'X < '  + dataFim;
        elif (ultimaDataNormalizada[:4] == 'X > ' ):
            data =  ultimaDataNormalizada.replace('X > ','');
    
            
            campos = found.split(' ');
            years  = campos[0];
            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_AFTER)

            return 'X > '  + dataFim;
    
        else:
            data =  ultimaDataNormalizada;
    
            campos = found.split(' ');
            years  = campos[0];

            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_AFTER)
            
            return dataFim;
        
def __X_YEARS_LATER     (foundList, listNorm):
    for found in foundList:
        ultimaDataNormalizada = listNorm[len(listNorm)-1]
        if (ultimaDataNormalizada.find(' < X < ') != -1):
            datas = ultimaDataNormalizada.split(' < X < ');
            #data1 = datas[0];
            data2 = datas[1];
            
            campos = found.split(' ');
            years  = campos[0];
            data2Fim = __DataNormalizada(data2, years, __ANO, __FLAG_AFTER)
                
            
            return data2Fim;
            
        elif (ultimaDataNormalizada[:4] == 'X < ' ):
            data =  ultimaDataNormalizada.replace('X < ','');
    
            campos = found.split(' ');
            years  = campos[0];
            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_AFTER)

            return 'X < '  + dataFim;
        elif (ultimaDataNormalizada[:4] == 'X > ' ):
            data =  ultimaDataNormalizada.replace('X > ','');
    
            campos = found.split(' ');
            years  = campos[0];

            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_AFTER)
            
            return 'X > '  + dataFim;
    
        else:
            data =  ultimaDataNormalizada;
    
            campos = found.split(' ');
            years  = campos[0];

            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_AFTER)
            
            return dataFim;
        
def __X_YEARS_AFTER     (foundList, listNorm):
    for found in foundList:
        ultimaDataNormalizada = listNorm[len(listNorm)-1]
        if (ultimaDataNormalizada.find(' < X < ') != -1):
            datas = ultimaDataNormalizada.split(' < X < ');
            #data1 = datas[0];
            data2 = datas[1];
            
            campos = found.split(' ');
            years  = campos[0];

            data2Fim = __DataNormalizada(data2, years, __ANO, __FLAG_AFTER)
            return data2Fim;
            
        elif (ultimaDataNormalizada[:4] == 'X < ' ):
            data =  ultimaDataNormalizada.replace('X < ','');
    
            campos = found.split(' ');
            years  = campos[0];
            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_AFTER)
            
            return 'X < '  + dataFim;
        elif (ultimaDataNormalizada[:4] == 'X > ' ):
            data =  ultimaDataNormalizada.replace('X > ','');
    
            
            campos = found.split(' ');
            years  = campos[0];
            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_AFTER)
            
            return 'X > '  + dataFim;
    
        else:
            data =  ultimaDataNormalizada;
    
            campos = found.split(' ');
            years  = campos[0];
            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_AFTER)
            
            return dataFim;
def __AFTER_X_YEARS     (foundList, listNorm):
    for found in foundList:
    
        ultimaDataNormalizada = listNorm[len(listNorm)-1]
        if (ultimaDataNormalizada.find(' < X < ') != -1):
            datas = ultimaDataNormalizada.split(' < X < ');
            #data1 = datas[0];
            data2 = datas[1];
            
            campos = found.split(' ');
            years  = campos[1];
            data2Fim = __DataNormalizada(data2, years, __ANO, __FLAG_AFTER)
            return data2Fim;
            
        elif (ultimaDataNormalizada[:4] == 'X < ' ):
            data =  ultimaDataNormalizada.replace('X < ','');
    
            campos = found.split(' ');
            years  = campos[1];
            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_AFTER)
            
            return 'X < '  + dataFim;
        elif (ultimaDataNormalizada[:4] == 'X > ' ):
            data =  ultimaDataNormalizada.replace('X > ','');
    
            campos = found.split(' ');
            years  = campos[1];
            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_AFTER)
    
        else:
            data =  ultimaDataNormalizada;
    
            campos = found.split(' ');
            years  = campos[1];
            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_AFTER)
            return dataFim;
def __BEFORE_X_YEARS    (foundList, listNorm):
    for found in foundList:

        ultimaDataNormalizada = listNorm[len(listNorm)-1]
        if (ultimaDataNormalizada.find(' < X < ') != -1):
            datas = ultimaDataNormalizada.split(' < X < ');
            data1 = datas[0];
            #data2 = datas[1];
            
            campos = found.split(' ');
            years  = campos[1];
            data1Fim = __DataNormalizada(data1, years, __ANO, __FLAG_BEFORE)
            return data1Fim;
        elif (ultimaDataNormalizada[:4] == 'X < ' ):
            data =  ultimaDataNormalizada.replace('X < ','');
            
            campos = found.split(' ');
            years  = campos[1];
            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_BEFORE)
            
            return 'X < '  + dataFim;
        elif (ultimaDataNormalizada[:4] == 'X > ' ):
            data =  ultimaDataNormalizada.replace('X > ','');
            campos = found.split(' ');
            years  = campos[1];
            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_BEFORE)
            return 'X > '  + dataFim;
    
        else:
            data =  ultimaDataNormalizada;
    
            campos = found.split(' ');
            years  = campos[1];
            dataFim = __DataNormalizada(data, years, __ANO, __FLAG_BEFORE)
            
            return dataFim;
def __X_MONTHS_BEFORE   (foundList, listNorm):
    for found in foundList:
    
        ultimaDataNormalizada = listNorm[len(listNorm)-1]
        if (ultimaDataNormalizada.find(' < X < ') != -1):
            datas = ultimaDataNormalizada.split(' < X < ');
            data1 = datas[0];
            
            
            campos = found.split(' ');
            monthsCalc  = campos[0];

            retorno1 = __DataNormalizada(data1, monthsCalc, __MES, __FLAG_BEFORE)
                
            return retorno1;
    
        elif (ultimaDataNormalizada[:4] == 'X < ' ):
            data =  ultimaDataNormalizada.replace('X < ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            monthsCalc  = campos[0];
            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_BEFORE)
            return 'X < '  + retorno;
        elif (ultimaDataNormalizada[:4] == 'X > ' ):
            data =  ultimaDataNormalizada.replace('X > ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            monthsCalc  = campos[0];
            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_BEFORE)

            return 'X > '  + retorno;
    
        else:
            data =  ultimaDataNormalizada;
            
            campos = found.split(' ');
            monthsCalc  = campos[0];
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());

            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_BEFORE)

            return retorno;

def __X_MONTHS_EARLY    (foundList, listNorm):
    for found in foundList:

        ultimaDataNormalizada = listNorm[len(listNorm)-1]
        if (ultimaDataNormalizada.find(' < X < ') != -1):
            datas = ultimaDataNormalizada.split(' < X < ');
            data1 = datas[0];
            campos = found.split(' ');
            monthsCalc  = campos[0];
            retorno1 = __DataNormalizada(data1, monthsCalc, __MES, __FLAG_BEFORE)
            return retorno1;
    
        elif (ultimaDataNormalizada[:4] == 'X < ' ):
            data =  ultimaDataNormalizada.replace('X < ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            monthsCalc  = campos[0];
            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_BEFORE)
            

            return 'X < '  + retorno;
        elif (ultimaDataNormalizada[:4] == 'X > ' ):
            data =  ultimaDataNormalizada.replace('X > ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            monthsCalc  = campos[0];
            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_BEFORE)
            

            return 'X > '  + retorno;
    
        else:
            data =  ultimaDataNormalizada;
            
            campos = found.split(' ');
            monthsCalc  = campos[0];
            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_BEFORE)

            return retorno;
def __X_MONTHS_LATE     (foundList, listNorm):
    for found in foundList:

        ultimaDataNormalizada = listNorm[len(listNorm)-1]
        if (ultimaDataNormalizada.find(' < X < ') != -1):
            datas = ultimaDataNormalizada.split(' < X < ');
            data2 = datas[1];
            
            
            campos = found.split(' ');
            monthsCalc  = campos[0];
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());

            retorno2 = __DataNormalizada(data2, monthsCalc, __MES, __FLAG_AFTER)
                
            return retorno2;
    
        elif (ultimaDataNormalizada[:4] == 'X < ' ):
            data =  ultimaDataNormalizada.replace('X < ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            monthsCalc  = campos[0];
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());
            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_AFTER)
            

            return 'X < '  + retorno;
        elif (ultimaDataNormalizada[:4] == 'X > ' ):
            data =  ultimaDataNormalizada.replace('X > ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            monthsCalc  = campos[0];
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());
            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_AFTER)
            

            return 'X > '  + retorno;
    
        else:
            data =  ultimaDataNormalizada;
            
            campos = found.split(' ');
            monthsCalc  = campos[0];
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());
            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_AFTER)

            return retorno;
def __X_MONTHS_LATER    (foundList, listNorm):
    for found in foundList:

        ultimaDataNormalizada = listNorm[len(listNorm)-1]
        if (ultimaDataNormalizada.find(' < X < ') != -1):
            datas = ultimaDataNormalizada.split(' < X < ');
            #data1 = datas[0];
            data2 = datas[1];
            
            
            campos = found.split(' ');
            monthsCalc  = campos[0];
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());

            retorno2 = __DataNormalizada(data2, monthsCalc, __MES, __FLAG_AFTER)
                
            return retorno2;
    
        elif (ultimaDataNormalizada[:4] == 'X < ' ):
            data =  ultimaDataNormalizada.replace('X < ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            monthsCalc  = campos[0];
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());
            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_AFTER)
            return 'X < '  + retorno;
        elif (ultimaDataNormalizada[:4] == 'X > ' ):
            data =  ultimaDataNormalizada.replace('X > ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            monthsCalc  = campos[0];
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());
            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_AFTER)
            return 'X > '  + retorno;
    
        else:
            data =  ultimaDataNormalizada;
            
            campos = found.split(' ');
            monthsCalc  = campos[0];
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());
            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_AFTER)

            return retorno;
def __X_MONTHS_AFTER    (foundList, listNorm):
    for found in foundList:

        ultimaDataNormalizada = listNorm[len(listNorm)-1]
        if (ultimaDataNormalizada.find(' < X < ') != -1):
            datas = ultimaDataNormalizada.split(' < X < ');
            #data1 = datas[0];
            data2 = datas[1];
            
            
            campos = found.split(' ');
            monthsCalc  = campos[0];
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());

            retorno2 = __DataNormalizada(data2, monthsCalc, __MES, __FLAG_AFTER)
                
            return retorno2;
    
        elif (ultimaDataNormalizada[:4] == 'X < ' ):
            data =  ultimaDataNormalizada.replace('X < ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            monthsCalc  = campos[0];
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());
            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_AFTER)
            

            return 'X < '  + retorno;
        elif (ultimaDataNormalizada[:4] == 'X > ' ):
            data =  ultimaDataNormalizada.replace('X > ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            monthsCalc  = campos[0];
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());
            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_AFTER)

            return 'X > '  + retorno;
    
        else:
            data =  ultimaDataNormalizada;
            
            campos = found.split(' ');
            monthsCalc  = campos[0];
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());
            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_AFTER)

            return retorno;
def __AFTER_X_MONTHS    (foundList, listNorm):
    for found in foundList:

        ultimaDataNormalizada = listNorm[len(listNorm)-1]
        if (ultimaDataNormalizada.find(' < X < ') != -1):
            datas = ultimaDataNormalizada.split(' < X < ');
            #data1 = datas[0];
            data2 = datas[1];
            
            
            campos = found.split(' ');
            monthsCalc  = campos[1];
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());

            retorno2 = __DataNormalizada(data2, monthsCalc, __MES, __FLAG_AFTER)
                
            return  retorno2;
    
        elif (ultimaDataNormalizada[:4] == 'X < ' ):
            data =  ultimaDataNormalizada.replace('X < ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            monthsCalc  = campos[1];
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());
            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_AFTER)
            

            return 'X < '  + retorno;
        elif (ultimaDataNormalizada[:4] == 'X > ' ):
            data =  ultimaDataNormalizada.replace('X > ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            monthsCalc  = campos[1];
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());
            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_AFTER)

            return 'X > '  + retorno;
    
        else:
            data =  ultimaDataNormalizada;
            
            campos = found.split(' ');
            monthsCalc  = campos[1];
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());
            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_AFTER)

            return retorno;
def __BEFORE_X_MONTHS   (foundList, listNorm):
    for found in foundList:

        ultimaDataNormalizada = listNorm[len(listNorm)-1]
        if (ultimaDataNormalizada.find(' < X < ') != -1):
            datas = ultimaDataNormalizada.split(' < X < ');
            data1 = datas[0];
            #data2 = datas[1];
            
            
            campos = found.split(' ');
            monthsCalc  = campos[1];
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());

            retorno1 = __DataNormalizada(data1, monthsCalc, __MES, __FLAG_BEFORE)
            return retorno1;
    
        elif (ultimaDataNormalizada[:4] == 'X < ' ):
            data =  ultimaDataNormalizada.replace('X < ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            monthsCalc  = campos[1];
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());
            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_BEFORE)

            return 'X < '  + retorno;
        elif (ultimaDataNormalizada[:4] == 'X > ' ):
            data =  ultimaDataNormalizada.replace('X > ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            monthsCalc  = campos[1];
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());
            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_BEFORE)

            return 'X > '  + retorno;
    
        else:
            data =  ultimaDataNormalizada;
            
            campos = found.split(' ');
            monthsCalc  = campos[1];
            if mapNumbers.has_key(str(monthsCalc).lower()):
                monthsCalc = mapNumbers.get(str(monthsCalc).lower());
            retorno = __DataNormalizada(data, monthsCalc, __MES, __FLAG_BEFORE)

            return retorno;
def __X_DAYS_BEFORE     (foundList, listNorm):
    for found in foundList:
    
        ultimaDataNormalizada = listNorm[len(listNorm)-1]
        if (ultimaDataNormalizada.find(' < X < ') != -1):
            datas = ultimaDataNormalizada.split(' < X < ');
            data1 = datas[0];
            #data2 = datas[1];
            
            
            campos = found.split(' ');
            daysCalc  = campos[0];
            retorno1 = __DataNormalizada(data1, daysCalc, __DIA, __FLAG_BEFORE)
            return retorno1;
    
        elif (ultimaDataNormalizada[:4] == 'X < ' ):
            data =  ultimaDataNormalizada.replace('X < ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            daysCalc  = campos[0];
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_BEFORE)

            return 'X < '  + retorno;
        elif (ultimaDataNormalizada[:4] == 'X > ' ):
            data =  ultimaDataNormalizada.replace('X > ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            daysCalc  = campos[0];
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_BEFORE)

            return 'X > '  + retorno;
    
        else:
            data =  ultimaDataNormalizada;
            
            campos = found.split(' ');
            daysCalc  = campos[0];
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_BEFORE)

            return retorno;
def __X_DAYS_EARLY      (foundList, listNorm):
    for found in foundList:

        ultimaDataNormalizada = listNorm[len(listNorm)-1]
        if (ultimaDataNormalizada.find(' < X < ') != -1):
            datas = ultimaDataNormalizada.split(' < X < ');
            data1 = datas[0];
            #data2 = datas[1];
            
            
            campos = found.split(' ');
            daysCalc  = campos[0];
            retorno1 = __DataNormalizada(data1, daysCalc, __DIA, __FLAG_BEFORE)
            return retorno1;
    
        elif (ultimaDataNormalizada[:4] == 'X < ' ):
            data =  ultimaDataNormalizada.replace('X < ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            daysCalc  = campos[0];
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_BEFORE)
            

            return 'X < '  + retorno;
        elif (ultimaDataNormalizada[:4] == 'X > ' ):
            data =  ultimaDataNormalizada.replace('X > ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            daysCalc  = campos[0];
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_BEFORE)

            return 'X > '  + retorno;
    
        else:
            data =  ultimaDataNormalizada;
            
            campos = found.split(' ');
            daysCalc  = campos[0];
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_BEFORE)

            return retorno;
def __X_DAYS_LATE       (foundList, listNorm):
    for found in foundList:

        ultimaDataNormalizada = listNorm[len(listNorm)-1]
        if (ultimaDataNormalizada.find(' < X < ') != -1):
            datas = ultimaDataNormalizada.split(' < X < ');
            #data1 = datas[0];
            data2 = datas[1];
            
            
            campos = found.split(' ');
            daysCalc  = campos[0];

            retorno2 = __DataNormalizada(data2, daysCalc, __DIA, __FLAG_AFTER)
                
            return retorno2;
    
        elif (ultimaDataNormalizada[:4] == 'X < ' ):
            data =  ultimaDataNormalizada.replace('X < ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            daysCalc  = campos[0];
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_AFTER)

            return 'X < '  + retorno;
        elif (ultimaDataNormalizada[:4] == 'X > ' ):
            data =  ultimaDataNormalizada.replace('X > ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            daysCalc  = campos[0];
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_AFTER)
            

            return 'X > '  + retorno;
    
        else:
            data =  ultimaDataNormalizada;  
            
            campos = found.split(' ');
            daysCalc  = campos[0];
            if mapNumbers.has_key(str(daysCalc).lower()):
                daysCalc = mapNumbers.get(str(daysCalc).lower());
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_AFTER)

            return retorno;
def __X_DAYS_LATER      (foundList, listNorm):
    for found in foundList:
    
        ultimaDataNormalizada = listNorm[len(listNorm)-1]
        if (ultimaDataNormalizada.find(' < X < ') != -1):
            datas = ultimaDataNormalizada.split(' < X < ');
            #data1 = datas[0];
            data2 = datas[1];
            
            
            campos = found.split(' ');
            daysCalc  = campos[0];
            retorno2 = __DataNormalizada(data2, daysCalc, __DIA, __FLAG_AFTER)
                
            return retorno2;
    
        elif (ultimaDataNormalizada[:4] == 'X < ' ):
            data =  ultimaDataNormalizada.replace('X < ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            daysCalc  = campos[0];
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_AFTER)

            return 'X < '  + retorno;
        elif (ultimaDataNormalizada[:4] == 'X > ' ):
            data =  ultimaDataNormalizada.replace('X > ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            daysCalc  = campos[0];
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_AFTER)

            return 'X > '  + retorno;
    
        else:
            data =  ultimaDataNormalizada;
            
            campos = found.split(' ');
            daysCalc  = campos[0];
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_AFTER)

            return retorno;
def __X_DAYS_AFTER      (foundList, listNorm):
    for found in foundList:

        ultimaDataNormalizada = listNorm[len(listNorm)-1]
        if (ultimaDataNormalizada.find(' < X < ') != -1):
            datas = ultimaDataNormalizada.split(' < X < ');
            #data1 = datas[0];
            data2 = datas[1];
            
            
            campos = found.split(' ');
            daysCalc  = campos[0];
            retorno2 = __DataNormalizada(data2, daysCalc, __DIA, __FLAG_AFTER)
    
            return retorno2
        elif (ultimaDataNormalizada[:4] == 'X < ' ):
            data =  ultimaDataNormalizada.replace('X < ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            daysCalc  = campos[0];
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_AFTER)
            

            return 'X < '  + retorno;
        elif (ultimaDataNormalizada[:4] == 'X > ' ):
            data =  ultimaDataNormalizada.replace('X > ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            daysCalc  = campos[0];
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_AFTER)

            return 'X > '  + retorno;
    
        else:
            data =  ultimaDataNormalizada;
            
            campos = found.split(' ');
            daysCalc  = campos[0];
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_AFTER)

            return retorno;
def __AFTER_X_DAYS      (foundList, listNorm):
    for found in foundList:

        ultimaDataNormalizada = listNorm[len(listNorm)-1]
        if (ultimaDataNormalizada.find(' < X < ') != -1):
            datas = ultimaDataNormalizada.split(' < X < ');
            #data1 = datas[0];
            data2 = datas[1];
            
            
            campos = found.split(' ');
            daysCalc  = campos[1];
            retorno2 = __DataNormalizada(data2, daysCalc, __DIA, __FLAG_AFTER)
                
            return retorno2;
    
        elif (ultimaDataNormalizada[:4] == 'X < ' ):
            data =  ultimaDataNormalizada.replace('X < ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            daysCalc  = campos[1];
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_AFTER)
            

            return 'X < '  + retorno;
        elif (ultimaDataNormalizada[:4] == 'X > ' ):
            data =  ultimaDataNormalizada.replace('X > ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            daysCalc  = campos[1];
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_AFTER)

            return 'X > '  + retorno;
    
        else:
            data =  ultimaDataNormalizada;
            
            campos = found.split(' ');
            daysCalc  = campos[1];
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_AFTER)

            return retorno;
def __BEFORE_X_DAYS     (foundList, listNorm):
    for found in foundList:

        ultimaDataNormalizada = listNorm[len(listNorm)-1]
        if (ultimaDataNormalizada.find(' < X < ') != -1):
            datas = ultimaDataNormalizada.split(' < X < ');
            data1 = datas[0];
            #data2 = datas[1];
            
            
            campos = found.split(' ');
            daysCalc  = campos[1];
            retorno1 = __DataNormalizada(data1, daysCalc, __DIA, __FLAG_BEFORE)
            return retorno1;
    
        elif (ultimaDataNormalizada[:4] == 'X < ' ):
            data =  ultimaDataNormalizada.replace('X < ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            daysCalc  = campos[1];
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_BEFORE)
            

            return 'X < '  + retorno;
        elif (ultimaDataNormalizada[:4] == 'X > ' ):
            data =  ultimaDataNormalizada.replace('X > ','');
    
            data = datas[0];
            
            
            campos = found.split(' ');
            daysCalc  = campos[1];
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_BEFORE)

            return 'X > '  + retorno;
    
        else:
            data =  ultimaDataNormalizada;
            
            campos = found.split(' ');
            daysCalc  = campos[1];
            retorno = __DataNormalizada(data, daysCalc, __DIA, __FLAG_BEFORE)
            return retorno;


def __EBT_GET_DATA     (foundList, listNorm, regex):
    for found in foundList:

        ultimaDataNormalizada = listNorm[len(listNorm)-1]
        if(ultimaDataNormalizada == ""):
            
                retorno = ""
                if (regex == __ANO_INDEFINIDO_EX):
                    camposAux = found.split("-")
                    if (camposAux[1] not in mesesNumericos):
                        camposAux[1] = meses[camposAux[1].lower()]
                    
                    retorno = camposAux[0] + "-" + camposAux[1] + "-[?]"
                elif (regex == __MES_INDEFINIDO_EX):
                    camposAux = found.split("-")
                    retorno = camposAux[0] + "-[?]-" + camposAux[2]
                elif (regex == __DIA_INDEFINIDO_EX):
                    camposAux = found.split("-")
                    if (camposAux[1] not in mesesNumericos):
                        camposAux[1] = meses[camposAux[1].lower()]
                    
                    retorno = "[?]-" + camposAux[1] + "-" + camposAux[0]            
            
        else:
            
            if (ultimaDataNormalizada.find(' < X < ') != -1):
                
                datas = ultimaDataNormalizada.split(' < X < ');
                data1 = datas[1];
                #data2 = datas[1];
                
                retorno = ""
                if (regex == __ANO_INDEFINIDO_EX):
                    anoAux= data1.split("-")[2];
                    camposAux = found.split("-")
                    if (camposAux[1] not in mesesNumericos):
                        camposAux[1] = meses[camposAux[1].lower()]
                    retorno = camposAux[0] + "-" + camposAux[1] + "-" + anoAux
                elif (regex == __MES_INDEFINIDO_EX):
                    mesAux= data1.split("-")[1];
                    camposAux = found.split("-")
                    retorno = camposAux[0] + "-" + mesAux + "-" + camposAux[2]
                elif (regex == __DIA_INDEFINIDO_EX):
                    diaAux= data1.split("-")[0];
                    camposAux = found.split("-")
                    if (camposAux[1] not in mesesNumericos):
                        camposAux[1] = meses[camposAux[1].lower()]                
                    retorno = diaAux + "-" + camposAux[1] + "-" + camposAux[0]
                    
                return retorno;
        
            elif (ultimaDataNormalizada[:4] == 'X < ' ):
                data =  ultimaDataNormalizada.replace('X < ','');
        
                data = datas[0];
                
                retorno = ""
                if (regex == __ANO_INDEFINIDO_EX):
                    anoAux= data.split("-")[2];
                    camposAux = found.split("-")
                    if (camposAux[1] not in mesesNumericos):
                        camposAux[1] = meses[camposAux[1].lower()]                
                    retorno = camposAux[0] + "-" + camposAux[1] + "-" + anoAux
                elif (regex == __MES_INDEFINIDO_EX):
                    mesAux= data.split("-")[1];
                    camposAux = found.split("-")
                    retorno = camposAux[0] + "-" + mesAux + "-" + camposAux[2]
                elif (regex == __DIA_INDEFINIDO_EX):
                    diaAux= data.split("-")[0];
                    camposAux = found.split("-")
                    if (camposAux[1] not in mesesNumericos):
                        camposAux[1] = meses[camposAux[1].lower()]                
                    retorno = diaAux + "-" + camposAux[1] + "-" + camposAux[0]
                
                return retorno;
                
            elif (ultimaDataNormalizada[:4] == 'X > ' ):
                data =  ultimaDataNormalizada.replace('X > ','');
        
                data = datas[0];
                
    
                retorno = ""
                if (regex == __ANO_INDEFINIDO_EX):
                    anoAux= data.split("-")[2];
                    camposAux = found.split("-")
                    if (camposAux[1] not in mesesNumericos):
                        camposAux[1] = meses[camposAux[1].lower()]
                    
                    retorno = camposAux[0] + "-" + camposAux[1] + "-" + anoAux
                elif (regex == __MES_INDEFINIDO_EX):
                    mesAux= data.split("-")[1];
                    camposAux = found.split("-")
                    retorno = camposAux[0] + "-" + mesAux + "-" + camposAux[2]
                elif (regex == __DIA_INDEFINIDO_EX):
                    diaAux= data.split("-")[0];
                    camposAux = found.split("-")
                    if (camposAux[1] not in mesesNumericos):
                        camposAux[1] = meses[camposAux[1].lower()]
                    
                    retorno = diaAux + "-" + camposAux[1] + "-" + camposAux[0]
                
                return retorno;
        
            else:
                data =  ultimaDataNormalizada;
                
    
                retorno = ""
                if (regex == __ANO_INDEFINIDO_EX):
                    anoAux= data.split("-")[2];
                    camposAux = found.split("-")
                    if (camposAux[1] not in mesesNumericos):
                        camposAux[1] = meses[camposAux[1].lower()]
                    
                    retorno = camposAux[0] + "-" + camposAux[1] + "-" + anoAux
                elif (regex == __MES_INDEFINIDO_EX):
                    mesAux= data.split("-")[1];
                    camposAux = found.split("-")
                    retorno = camposAux[0] + "-" + mesAux + "-" + camposAux[2]
                elif (regex == __DIA_INDEFINIDO_EX):
                    diaAux= data.split("-")[0];
                    camposAux = found.split("-")
                    if (camposAux[1] not in mesesNumericos):
                        camposAux[1] = meses[camposAux[1].lower()]
                    
                    retorno = diaAux + "-" + camposAux[1] + "-" + camposAux[0]
            
            return retorno;

#20140416 - George Alves - FIM
#Retorna a expressão encontrada
def __ExpressionReturn(expression, text):
    reMDA = expression
    regMDA = re.compile(reMDA, re.IGNORECASE)
    found = regMDA.findall(text)
    result = ""
    for a in found:
        if len(a) > 1:
            result = result + a[0]
    
    return [a[0] for a in found if len(a) > 1]