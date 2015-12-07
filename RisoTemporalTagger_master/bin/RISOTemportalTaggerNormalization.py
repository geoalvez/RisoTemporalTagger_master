# coding: utf-8

'''
Created on 31/08/2012

@author: Adriano Santos

TODO: Realizar um refectory URGENTE nesta classe. Tudo que foi desenvolvido aqui foi, apenas, para análise da proposta.
'''
'''
Método utilizado normalizar as expressoes no formato
#"from" mes dia, ano "to" mes dia, ano 
Retornando o intervalo no formato : Data < X < Data.
'''

from datetime import datetime
import re


day_numbers = "(1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31)"
year = "((?<=\s)\d{4}|^\d{4})"
month = "(january|february|march|april|may|june|july|august|september|october|november|december)"
meses = {'january':'01','february':'02','march':'03','april':'04','may':'05','june':'06','july':'07','august':'08','september':'09','october':'10','november':'11','december':'12'}
qtdNum = "([0-9]+" #20140415 - George Alves

'Lista de Padrões Mapeados para normalização'
__AA_EX = "(" + year + " - " + year + ")" 
__FromMDAToMDA_EX = "(from " + month + " " + day_numbers + ", " + year + " to " + month + " " + day_numbers + ", " + year + ")"
__FromMDToMD_EX = "(from " + month + " " + day_numbers + " to " + month + " " + day_numbers + ")" 
__FromMToM_EX = "(from " + month + " to " + month + ")"
__MD_MD_EX = "(" + month + " " + day_numbers + " *- *" + month + " " + day_numbers + ")"
__MDA_EX = "(" + month + " " + day_numbers + ", *" + year + ")"
__AfterMDA_EX = "(after  " + month + " " + day_numbers + ", *" + year + ")"
__BeforeMDA_EX = "(before " + month + " " + day_numbers + ", *" + year + ")"
__DMA_EX = "(" + day_numbers + " " + month + " " + year + ")" 
__MA_EX = "(" + month + " " + year + ")" 
__MD_EX = "(" + month + " " + day_numbers + ")" 
# 20140415 - George Alves - INICIO 
__X_YEARS_BEFORE_EX = "("+qtdNum+" year[s]* before)"
__X_YEARS_EARLY_EX  = "("+qtdNum+" year[s]* early)"
__X_YEARS_LATE_EX   = "("+qtdNum+" year[s]* late)"
__X_YEARS_LATER_EX  = "("+qtdNum+" year[s]* later)"
__X_YEARS_AFTER_EX  = "("+qtdNum+" year[s]* after)"
__AFTER_X_YEARS_EX  = "(after "+qtdNum+" year[s]*)"
__BEFORE_X_YEARS_EX = "(before "+qtdNum+" year[s]*)"

__X_MONTHS_BEFORE_EX = "("+qtdNum+" month[s]* before)"
__X_MONTHS_EARLY_EX  = "("+qtdNum+" month[s]* early)"
__X_MONTHS_LATE_EX   = "("+qtdNum+" month[s]* late)"
__X_MONTHS_LATER_EX  = "("+qtdNum+" month[s]* later)"
__X_MONTHS_AFTER_EX  = "("+qtdNum+" month[s]* after)"
__AFTER_X_MONTHS_EX  = "(after "+qtdNum+" month[s]*)"
__BEFORE_X_MONTHS_EX = "(before "+qtdNum+" month[s]*)"

__X_DAYS_BEFORE_EX = "("+qtdNum+" day[s]* before)"
__X_DAYS_EARLY_EX  = "("+qtdNum+" day[s]* early)"
__X_DAYS_LATE_EX   = "("+qtdNum+" day[s]* late)"
__X_DAYS_LATER_EX  = "("+qtdNum+" day[s]* later)"
__X_DAYS_AFTER_EX  = "("+qtdNum+" day[s]* after)"
__AFTER_X_DAYS_EX  = "(after "+qtdNum+" day[s]*)"
__BEFORE_X_DAYS_EX = "(before "+qtdNum+" day[s]*)"


# 20140415 - George Alves - FIM 


# Normalização de valores
def Normalization(text):
    #Inicia um array com todos os padrões mapeados
    #20140415 - George Alves- Inclusao dos novos padroes - INICIO 
    arrayFromEx = [__AA_EX, __FromMDAToMDA_EX, __FromMDToMD_EX, __FromMToM_EX, __MD_MD_EX, __MDA_EX, __AfterMDA_EX, __BeforeMDA_EX, __DMA_EX, __MA_EX, __MD_EX, __X_YEARS_BEFORE_EX,__X_YEARS_EARLY_EX ,__X_YEARS_LATE_EX  ,__X_YEARS_LATER_EX ,__X_YEARS_AFTER_EX ,__AFTER_X_YEARS_EX ,__BEFORE_X_YEARS_EX, __X_MONTHS_BEFORE_EX , __X_MONTHS_EARLY_EX  , __X_MONTHS_LATE_EX   , __X_MONTHS_LATER_EX  , __X_MONTHS_AFTER_EX  , __AFTER_X_MONTHS_EX  , __BEFORE_X_MONTHS_EX , __X_DAYS_BEFORE_EX   , __X_DAYS_EARLY_EX    , __X_DAYS_LATE_EX     , __X_DAYS_LATER_EX    , __X_DAYS_AFTER_EX    , __AFTER_X_DAYS_EX    , __BEFORE_X_DAYS_EX] 
    #20140415 - George Alves- Inclusao dos novos padroes - FIM 
    value = None
    for regex in arrayFromEx:
        list = __ExpressionReturn(regex, text)
        if len(list) > 0:
            return __NormalizedValue(regex, list)

def NormalizationListAnteriores(text, listNorm):
    #Inicia um array com todos os padrões mapeados
    #20140415 - George Alves- Inclusao dos novos padroes - INICIO 
    arrayFromEx = [ __X_YEARS_BEFORE_EX,__X_YEARS_EARLY_EX ,__X_YEARS_LATE_EX  ,__X_YEARS_LATER_EX ,__X_YEARS_AFTER_EX ,__AFTER_X_YEARS_EX ,__BEFORE_X_YEARS_EX, __X_MONTHS_BEFORE_EX , __X_MONTHS_EARLY_EX  , __X_MONTHS_LATE_EX   , __X_MONTHS_LATER_EX  , __X_MONTHS_AFTER_EX  , __AFTER_X_MONTHS_EX  , __BEFORE_X_MONTHS_EX , __X_DAYS_BEFORE_EX   , __X_DAYS_EARLY_EX    , __X_DAYS_LATE_EX     , __X_DAYS_LATER_EX    , __X_DAYS_AFTER_EX    , __AFTER_X_DAYS_EX    , __BEFORE_X_DAYS_EX] 
    #20140415 - George Alves- Inclusao dos novos padroes - FIM 
    
    value = None
    for regex in arrayFromEx:
        list = __ExpressionReturn(regex, text)
        if len(list) > 0:
            return __NormalizedValueListNorm(regex, list, listNorm)

            
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

#20140416 - George Alves - INICIO 
def __NormalizedValueListNorm(regex, found, listNorm):
    if regex == __X_YEARS_BEFORE_EX:
        return __X_YEARS_BEFORE(found,listNorm)
    elif regex == __X_YEARS_EARLY_EX:
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
    


    elif regex == __X_MONTHS_BEFORE_EX:
        return __X_MONTHS_BEFORE(found,listNorm)
    elif regex == __X_MONTHS_EARLY_EX:
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
#20140416 - George Alves - FRIM 
    
def __FromMDAToMDA(found):
     for risotime in found:
         risotime = risotime.replace('from ', '')
         datas = risotime.split(' to ');
         dt1=datetime.strptime(datas[0], '%B %d, %Y')
         dt2=datetime.strptime(datas[1], '%B %d, %Y')
         # a= dt1.strftime('%d-%m-%Y')
         a = (dt1.isoformat().split('T')[0]).split('-')[2]+"-"+ (dt1.isoformat().split('T')[0]).split('-')[1]+"-"+(dt1.isoformat().split('T')[0]).split('-')[0]

         # b= dt2.strftime('%d-%m-%Y')
         b = (dt2.isoformat().split('T')[0]).split('-')[2]+"-"+ (dt2.isoformat().split('T')[0]).split('-')[1]+"-"+(dt2.isoformat().split('T')[0]).split('-')[0]

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
        return meses[datas[0].lower()] + '-' + datas[1]

# Expressões para o padrão mes dia
def __MD(found):
    for risotime in found:
        datas = risotime.split(' ')
        return datas[1] + '-' + meses[datas[0].lower()] + '-XXXX' 



#"from" mes "to" mes : Data < X < Data -- Pegar ano corrente    
def __FromMToM(found):
       
       hoje = datetime.today()
       ano = str(hoje.year)
       
       for risotime in found:
           risotime = risotime.replace('from ', '')
           datas = risotime.split(' to ');
           
           a = 'xx-' + meses[datas[0].lower()] + '-' + ano
           b = 'xx-' + meses[datas[1].lower()] + '-' +  ano
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
        #return dt.strftime('%d-%m-%Y')
        return (dt.isoformat().split('T')[0]).split('-')[2]+"-"+ (dt.isoformat().split('T')[0]).split('-')[1]+"-"+(dt.isoformat().split('T')[0]).split('-')[0] 

#Para intervalor anterior aa dada encontrada
def __AfterMDA(found):
    for risotime in found:
        risotime = risotime.replace('after ','')
        dt=datetime.strptime(risotime, '%B %d, %Y')
        # return 'X < ' + dt.strftime('%d-%m-%Y')
        return 'X < ' + (dt.isoformat().split('T')[0]).split('-')[2]+"-"+ (dt.isoformat().split('T')[0]).split('-')[1]+"-"+(dt.isoformat().split('T')[0]).split('-')[0]

#Para intervalor posterior aa dada encontrada
def __BeforeMDA(found):
    for risotime in found:
        risotime = risotime.replace('after ','')
        dt=datetime.strptime(risotime, '%B %d, %Y')
        #return 'X < ' + dt.strftime('%d-%m-%Y')
        return 'X < ' + (dt.isoformat().split('T')[0]).split('-')[2]+"-"+ (dt.isoformat().split('T')[0]).split('-')[1]+"-"+(dt.isoformat().split('T')[0]).split('-')[0]

#Para datas no formato dia mes ano
def __DMA(found):
    for risotime in found:
        dt=datetime.strptime(risotime, '%d %B %Y')
        # return dt.strftime('%d-%m-%Y')
        return (dt.isoformat().split('T')[0]).split('-')[2]+"-"+ (dt.isoformat().split('T')[0]).split('-')[1]+"-"+(dt.isoformat().split('T')[0]).split('-')[0]

#Para datas no formato ano - ano OU ano-ano
def __AA(found):
    for risotime in found:
        if (risotime.find(' - ') != -1):
           datas = risotime.split(' - ');
        elif (risotime.find('-') != -1):
           datas = risotime.split('-');
        return datas[0] + ' < X < ' + datas[1]

#20140416 - George Alves - INICIO
def __X_YEARS_BEFORE    (found, listNorm):
    ultimaDataNormalizada = listNorm[len(listNorm)-1]
    if (ultimaDataNormalizada.find(' < X < ') != -1):
        datas = ultimaDataNormalizada.split(' < X < ');
        data1 = datas[0];
        data2 = datas[1];
        
        dia1 = data1.split('-')[0]; 
        mes1 = data1.split('-')[1]; 
        ano1 = data1.split('-')[2]; 
        
        dia2 = data2.split('-')[0]; 
        mes2 = data2.split('-')[1]; 
        ano2 = data2.split('-')[2];
        
        campos = found.split(' ');
        yearsBefore  = campos[0];
        
        ano1Sub = ano1 - yearsBefore;
        ano2Sub = ano2 - yearsBefore;
        
        
        data1Fim = dia1 + mes1 + ano1Sub;
        data2Fim = dia2 + mes2 + ano2Sub;
        
        return data1Fim + ' < X < ' + data2Fim;
        
    elif (ultimaDataNormalizada[:4] == 'X < ' ):
        data =  ultimaDataNormalizada.replace('X < ','');

        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        yearsBefore  = campos[0];
        
        anoSub = ano - yearsBefore;
        
        
        dataFim = dia + mes + anoSub;
        
        return 'X < '  + dataFim;

    else:
        data =  ultimaDataNormalizada;

        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        yearsBefore  = campos[0];
        
        anoSub = ano - yearsBefore;
        
        
        dataFim = dia + mes + anoSub;
        
        return dataFim;
                
def __X_YEARS_EARLY     (found, listNorm):

    ultimaDataNormalizada = listNorm[len(listNorm)-1]
    if (ultimaDataNormalizada.find(' < X < ') != -1):
        datas = ultimaDataNormalizada.split(' < X < ');
        data1 = datas[0];
        data2 = datas[1];
        
        dia1 = data1.split('-')[0]; 
        mes1 = data1.split('-')[1]; 
        ano1 = data1.split('-')[2]; 
        
        dia2 = data2.split('-')[0]; 
        mes2 = data2.split('-')[1]; 
        ano2 = data2.split('-')[2];
        
        campos = found.split(' ');
        yearsBefore  = campos[0];
        
        ano1Sub = ano1 - yearsBefore;
        ano2Sub = ano2 - yearsBefore;
        
        
        data1Fim = dia1 + mes1 + ano1Sub;
        data2Fim = dia2 + mes2 + ano2Sub;
        
        return data1Fim + ' < X < ' + data2Fim;
        
    elif (ultimaDataNormalizada[:4] == 'X < ' ):
        data =  ultimaDataNormalizada.replace('X < ','');

        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        yearsBefore  = campos[0];
        
        anoSub = ano - yearsBefore;
        
        
        dataFim = dia + mes + anoSub;
        
        return 'X < '  + dataFim;

    else:
        data =  ultimaDataNormalizada;

        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        yearsBefore  = campos[0];
        
        anoSub = ano - yearsBefore;
        
        
        dataFim = dia + mes + anoSub;
        
        return dataFim;


def __X_YEARS_LATE      (found, listNorm):
    ultimaDataNormalizada = listNorm[len(listNorm)-1]
    if (ultimaDataNormalizada.find(' < X < ') != -1):
        datas = ultimaDataNormalizada.split(' < X < ');
        data1 = datas[0];
        data2 = datas[1];
        
        dia1 = data1.split('-')[0]; 
        mes1 = data1.split('-')[1]; 
        ano1 = data1.split('-')[2]; 
        
        dia2 = data2.split('-')[0]; 
        mes2 = data2.split('-')[1]; 
        ano2 = data2.split('-')[2];
        
        campos = found.split(' ');
        yearsAfter  = campos[0];
        
        ano1Sub = ano1 + yearsAfter;
        ano2Sub = ano2 + yearsAfter;
        
        
        data1Fim = dia1 + mes1 + ano1Sub;
        data2Fim = dia2 + mes2 + ano2Sub;
        
        return data1Fim + ' < X < ' + data2Fim;
        
    elif (ultimaDataNormalizada[:4] == 'X < ' ):
        data =  ultimaDataNormalizada.replace('X < ','');

        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        yearsAfter  = campos[0];
        
        anoSub = ano + yearsAfter;
        
        
        dataFim = dia + mes + anoSub;
        
        return 'X < '  + dataFim;

    else:
        data =  ultimaDataNormalizada;

        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        yearsAfter  = campos[0];
        
        anoSub = ano + yearsAfter;
        
        
        dataFim = dia + mes + anoSub;
        
        return dataFim;
def __X_YEARS_LATER     (found, listNorm):
    ultimaDataNormalizada = listNorm[len(listNorm)-1]
    if (ultimaDataNormalizada.find(' < X < ') != -1):
        datas = ultimaDataNormalizada.split(' < X < ');
        data1 = datas[0];
        data2 = datas[1];
        
        dia1 = data1.split('-')[0]; 
        mes1 = data1.split('-')[1]; 
        ano1 = data1.split('-')[2]; 
        
        dia2 = data2.split('-')[0]; 
        mes2 = data2.split('-')[1]; 
        ano2 = data2.split('-')[2];
        
        campos = found.split(' ');
        yearsAfter  = campos[0];
        
        ano1Sub = ano1 + yearsAfter;
        ano2Sub = ano2 + yearsAfter;
        
        
        data1Fim = dia1 + mes1 + ano1Sub;
        data2Fim = dia2 + mes2 + ano2Sub;
        
        return data1Fim + ' < X < ' + data2Fim;
        
    elif (ultimaDataNormalizada[:4] == 'X < ' ):
        data =  ultimaDataNormalizada.replace('X < ','');

        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        yearsAfter  = campos[0];
        
        anoSub = ano + yearsAfter;
        
        
        dataFim = dia + mes + anoSub;
        
        return 'X < '  + dataFim;

    else:
        data =  ultimaDataNormalizada;

        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        yearsAfter  = campos[0];
        
        anoSub = ano + yearsAfter;
        
        
        dataFim = dia + mes + anoSub;
        
        return dataFim;
def __X_YEARS_AFTER     (found, listNorm):
    ultimaDataNormalizada = listNorm[len(listNorm)-1]
    if (ultimaDataNormalizada.find(' < X < ') != -1):
        datas = ultimaDataNormalizada.split(' < X < ');
        data1 = datas[0];
        data2 = datas[1];
        
        dia1 = data1.split('-')[0]; 
        mes1 = data1.split('-')[1]; 
        ano1 = data1.split('-')[2]; 
        
        dia2 = data2.split('-')[0]; 
        mes2 = data2.split('-')[1]; 
        ano2 = data2.split('-')[2];
        
        campos = found.split(' ');
        yearsAfter  = campos[0];
        
        ano1Sub = ano1 + yearsAfter;
        ano2Sub = ano2 + yearsAfter;
        
        
        data1Fim = dia1 + mes1 + ano1Sub;
        data2Fim = dia2 + mes2 + ano2Sub;
        
        return data1Fim + ' < X < ' + data2Fim;
        
    elif (ultimaDataNormalizada[:4] == 'X < ' ):
        data =  ultimaDataNormalizada.replace('X < ','');

        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        yearsAfter  = campos[0];
        
        anoSub = ano + yearsAfter;
        
        
        dataFim = dia + mes + anoSub;
        
        return 'X < '  + dataFim;

    else:
        data =  ultimaDataNormalizada;

        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        yearsAfter  = campos[0];
        
        anoSub = ano + yearsAfter;
        
        
        dataFim = dia + mes + anoSub;
        
        return dataFim;
def __AFTER_X_YEARS     (found, listNorm):
    ultimaDataNormalizada = listNorm[len(listNorm)-1]
    if (ultimaDataNormalizada.find(' < X < ') != -1):
        datas = ultimaDataNormalizada.split(' < X < ');
        data1 = datas[0];
        data2 = datas[1];
        
        dia1 = data1.split('-')[0]; 
        mes1 = data1.split('-')[1]; 
        ano1 = data1.split('-')[2]; 
        
        dia2 = data2.split('-')[0]; 
        mes2 = data2.split('-')[1]; 
        ano2 = data2.split('-')[2];
        
        campos = found.split(' ');
        yearsAfter  = campos[3];
        
        ano1Sub = ano1 + yearsAfter;
        ano2Sub = ano2 + yearsAfter;
        
        
        data1Fim = dia1 + mes1 + ano1Sub;
        data2Fim = dia2 + mes2 + ano2Sub;
        
        return data1Fim + ' < X < ' + data2Fim;
        
    elif (ultimaDataNormalizada[:4] == 'X < ' ):
        data =  ultimaDataNormalizada.replace('X < ','');

        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        yearsAfter  = campos[3];
        
        anoSub = ano + yearsAfter;
        
        
        dataFim = dia + mes + anoSub;
        
        return 'X < '  + dataFim;

    else:
        data =  ultimaDataNormalizada;

        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        yearsAfter  = campos[3];
        
        anoSub = ano + yearsAfter;
        
        
        dataFim = dia + mes + anoSub;
        
        return dataFim;
def __BEFORE_X_YEARS    (found, listNorm):
    ultimaDataNormalizada = listNorm[len(listNorm)-1]
    if (ultimaDataNormalizada.find(' < X < ') != -1):
        datas = ultimaDataNormalizada.split(' < X < ');
        data1 = datas[0];
        data2 = datas[1];
        
        dia1 = data1.split('-')[0]; 
        mes1 = data1.split('-')[1]; 
        ano1 = data1.split('-')[2]; 
        
        dia2 = data2.split('-')[0]; 
        mes2 = data2.split('-')[1]; 
        ano2 = data2.split('-')[2];
        
        campos = found.split(' ');
        yearsBefore  = campos[3];
        
        ano1Sub = ano1 - yearsBefore;
        ano2Sub = ano2 - yearsBefore;
        
        
        data1Fim = dia1 + mes1 + ano1Sub;
        data2Fim = dia2 + mes2 + ano2Sub;
        
        return data1Fim + ' < X < ' + data2Fim;
        
    elif (ultimaDataNormalizada[:4] == 'X < ' ):
        data =  ultimaDataNormalizada.replace('X < ','');

        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        yearsBefore  = campos[3];
        
        anoSub = ano - yearsBefore;
        
        
        dataFim = dia + mes + anoSub;
        
        return 'X < '  + dataFim;

    else:
        data =  ultimaDataNormalizada;

        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        yearsBefore  = campos[3];
        
        anoSub = ano - yearsBefore;
        
        
        dataFim = dia + mes + anoSub;
        
        return dataFim;
def __X_MONTHS_BEFORE   (found, listNorm):
    ultimaDataNormalizada = listNorm[len(listNorm)-1]
    if (ultimaDataNormalizada.find(' < X < ') != -1):
        datas = ultimaDataNormalizada.split(' < X < ');
        data1 = datas[0];
        data2 = datas[1];
        
        dia1 = data1.split('-')[0]; 
        mes1 = data1.split('-')[1]; 
        ano1 = data1.split('-')[2]; 
        
        dia2 = data2.split('-')[0]; 
        mes2 = data2.split('-')[1]; 
        ano2 = data2.split('-')[2];
        
        campos = found.split(' ');
        monthsCalc  = campos[0];
        daysCalc  = monthsCalc * 30;
        
        
        dataAux1 = datetime.date(ano1, mes1, dia1)
        dataAux2 = datetime.date(ano2, mes2, dia2)
        
        
        retorno1 = (dataAux1 - datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        retorno2 = (dataAux2 - datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        
        return retorno1 + ' < X < ' + retorno2;

    elif (ultimaDataNormalizada[:4] == 'X < ' ):
        data =  ultimaDataNormalizada.replace('X < ','');

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        monthsCalc  = campos[0];
        daysCalc  = monthsCalc * 30;
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux - datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')

        
        return 'X < '  + retorno;

    else:
        data =  ultimaDataNormalizada;

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        monthsCalc  = campos[0];
        daysCalc  = monthsCalc * 30;
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux - datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        return retorno;

def __X_MONTHS_EARLY    (found, listNorm):
    ultimaDataNormalizada = listNorm[len(listNorm)-1]
    if (ultimaDataNormalizada.find(' < X < ') != -1):
        datas = ultimaDataNormalizada.split(' < X < ');
        data1 = datas[0];
        data2 = datas[1];
        
        dia1 = data1.split('-')[0]; 
        mes1 = data1.split('-')[1]; 
        ano1 = data1.split('-')[2]; 
        
        dia2 = data2.split('-')[0]; 
        mes2 = data2.split('-')[1]; 
        ano2 = data2.split('-')[2];
        
        campos = found.split(' ');
        monthsCalc  = campos[0];
        daysCalc  = monthsCalc * 30;
        
        
        dataAux1 = datetime.date(ano1, mes1, dia1)
        dataAux2 = datetime.date(ano2, mes2, dia2)
        
        
        retorno1 = (dataAux1 - datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        retorno2 = (dataAux2 - datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        
        return retorno1 + ' < X < ' + retorno2;

    elif (ultimaDataNormalizada[:4] == 'X < ' ):
        data =  ultimaDataNormalizada.replace('X < ','');

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        monthsCalc  = campos[0];
        daysCalc  = monthsCalc * 30;
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux - datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')

        
        return 'X < '  + retorno;

    else:
        data =  ultimaDataNormalizada;

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        monthsCalc  = campos[0];
        daysCalc  = monthsCalc * 30;
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux - datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        return retorno;
def __X_MONTHS_LATE     (found, listNorm):
    ultimaDataNormalizada = listNorm[len(listNorm)-1]
    if (ultimaDataNormalizada.find(' < X < ') != -1):
        datas = ultimaDataNormalizada.split(' < X < ');
        data1 = datas[0];
        data2 = datas[1];
        
        dia1 = data1.split('-')[0]; 
        mes1 = data1.split('-')[1]; 
        ano1 = data1.split('-')[2]; 
        
        dia2 = data2.split('-')[0]; 
        mes2 = data2.split('-')[1]; 
        ano2 = data2.split('-')[2];
        
        campos = found.split(' ');
        monthsCalc  = campos[0];
        daysCalc  = monthsCalc * 30;
        
        
        dataAux1 = datetime.date(ano1, mes1, dia1)
        dataAux2 = datetime.date(ano2, mes2, dia2)
        
        
        retorno1 = (dataAux1 + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        retorno2 = (dataAux2 + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        
        return retorno1 + ' < X < ' + retorno2;

    elif (ultimaDataNormalizada[:4] == 'X < ' ):
        data =  ultimaDataNormalizada.replace('X < ','');

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        monthsCalc  = campos[0];
        daysCalc  = monthsCalc * 30;
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')

        
        return 'X < '  + retorno;

    else:
        data =  ultimaDataNormalizada;

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        monthsCalc  = campos[0];
        daysCalc  = monthsCalc * 30;
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        return retorno;
def __X_MONTHS_LATER    (found, listNorm):
    ultimaDataNormalizada = listNorm[len(listNorm)-1]
    if (ultimaDataNormalizada.find(' < X < ') != -1):
        datas = ultimaDataNormalizada.split(' < X < ');
        data1 = datas[0];
        data2 = datas[1];
        
        dia1 = data1.split('-')[0]; 
        mes1 = data1.split('-')[1]; 
        ano1 = data1.split('-')[2]; 
        
        dia2 = data2.split('-')[0]; 
        mes2 = data2.split('-')[1]; 
        ano2 = data2.split('-')[2];
        
        campos = found.split(' ');
        monthsCalc  = campos[0];
        daysCalc  = monthsCalc * 30;
        
        
        dataAux1 = datetime.date(ano1, mes1, dia1)
        dataAux2 = datetime.date(ano2, mes2, dia2)
        
        
        retorno1 = (dataAux1 + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        retorno2 = (dataAux2 + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        
        return retorno1 + ' < X < ' + retorno2;

    elif (ultimaDataNormalizada[:4] == 'X < ' ):
        data =  ultimaDataNormalizada.replace('X < ','');

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        monthsCalc  = campos[0];
        daysCalc  = monthsCalc * 30;
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')

        
        return 'X < '  + retorno;

    else:
        data =  ultimaDataNormalizada;

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        monthsCalc  = campos[0];
        daysCalc  = monthsCalc * 30;
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        return retorno;
def __X_MONTHS_AFTER    (found, listNorm):
    ultimaDataNormalizada = listNorm[len(listNorm)-1]
    if (ultimaDataNormalizada.find(' < X < ') != -1):
        datas = ultimaDataNormalizada.split(' < X < ');
        data1 = datas[0];
        data2 = datas[1];
        
        dia1 = data1.split('-')[0]; 
        mes1 = data1.split('-')[1]; 
        ano1 = data1.split('-')[2]; 
        
        dia2 = data2.split('-')[0]; 
        mes2 = data2.split('-')[1]; 
        ano2 = data2.split('-')[2];
        
        campos = found.split(' ');
        monthsCalc  = campos[0];
        daysCalc  = monthsCalc * 30;
        
        
        dataAux1 = datetime.date(ano1, mes1, dia1)
        dataAux2 = datetime.date(ano2, mes2, dia2)
        
        
        retorno1 = (dataAux1 + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        retorno2 = (dataAux2 + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        
        return retorno1 + ' < X < ' + retorno2;

    elif (ultimaDataNormalizada[:4] == 'X < ' ):
        data =  ultimaDataNormalizada.replace('X < ','');

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        monthsCalc  = campos[0];
        daysCalc  = monthsCalc * 30;
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')

        
        return 'X < '  + retorno;

    else:
        data =  ultimaDataNormalizada;

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        monthsCalc  = campos[0];
        daysCalc  = monthsCalc * 30;
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        return retorno;
def __AFTER_X_MONTHS    (found, listNorm):
    ultimaDataNormalizada = listNorm[len(listNorm)-1]
    if (ultimaDataNormalizada.find(' < X < ') != -1):
        datas = ultimaDataNormalizada.split(' < X < ');
        data1 = datas[0];
        data2 = datas[1];
        
        dia1 = data1.split('-')[0]; 
        mes1 = data1.split('-')[1]; 
        ano1 = data1.split('-')[2]; 
        
        dia2 = data2.split('-')[0]; 
        mes2 = data2.split('-')[1]; 
        ano2 = data2.split('-')[2];
        
        campos = found.split(' ');
        monthsCalc  = campos[1];
        daysCalc  = monthsCalc * 30;
        
        
        dataAux1 = datetime.date(ano1, mes1, dia1)
        dataAux2 = datetime.date(ano2, mes2, dia2)
        
        
        retorno1 = (dataAux1 + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        retorno2 = (dataAux2 + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        
        return retorno1 + ' < X < ' + retorno2;

    elif (ultimaDataNormalizada[:4] == 'X < ' ):
        data =  ultimaDataNormalizada.replace('X < ','');

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        monthsCalc  = campos[1];
        daysCalc  = monthsCalc * 30;
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')

        
        return 'X < '  + retorno;

    else:
        data =  ultimaDataNormalizada;

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        monthsCalc  = campos[1];
        daysCalc  = monthsCalc * 30;
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        return retorno;
def __BEFORE_X_MONTHS   (found, listNorm):
    ultimaDataNormalizada = listNorm[len(listNorm)-1]
    if (ultimaDataNormalizada.find(' < X < ') != -1):
        datas = ultimaDataNormalizada.split(' < X < ');
        data1 = datas[0];
        data2 = datas[1];
        
        dia1 = data1.split('-')[0]; 
        mes1 = data1.split('-')[1]; 
        ano1 = data1.split('-')[2]; 
        
        dia2 = data2.split('-')[0]; 
        mes2 = data2.split('-')[1]; 
        ano2 = data2.split('-')[2];
        
        campos = found.split(' ');
        monthsCalc  = campos[1];
        daysCalc  = monthsCalc * 30;
        
        
        dataAux1 = datetime.date(ano1, mes1, dia1)
        dataAux2 = datetime.date(ano2, mes2, dia2)
        
        
        retorno1 = (dataAux1 - datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        retorno2 = (dataAux2 - datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        
        return retorno1 + ' < X < ' + retorno2;

    elif (ultimaDataNormalizada[:4] == 'X < ' ):
        data =  ultimaDataNormalizada.replace('X < ','');

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        monthsCalc  = campos[1];
        daysCalc  = monthsCalc * 30;
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux - datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')

        
        return 'X < '  + retorno;

    else:
        data =  ultimaDataNormalizada;

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        monthsCalc  = campos[1];
        daysCalc  = monthsCalc * 30;
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux - datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        return retorno;
def __X_DAYS_BEFORE     (found, listNorm):
    ultimaDataNormalizada = listNorm[len(listNorm)-1]
    if (ultimaDataNormalizada.find(' < X < ') != -1):
        datas = ultimaDataNormalizada.split(' < X < ');
        data1 = datas[0];
        data2 = datas[1];
        
        dia1 = data1.split('-')[0]; 
        mes1 = data1.split('-')[1]; 
        ano1 = data1.split('-')[2]; 
        
        dia2 = data2.split('-')[0]; 
        mes2 = data2.split('-')[1]; 
        ano2 = data2.split('-')[2];
        
        campos = found.split(' ');
        daysCalc  = campos[0];
        
        
        dataAux1 = datetime.date(ano1, mes1, dia1)
        dataAux2 = datetime.date(ano2, mes2, dia2)
        
        
        retorno1 = (dataAux1 - datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        retorno2 = (dataAux2 - datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        
        return retorno1 + ' < X < ' + retorno2;

    elif (ultimaDataNormalizada[:4] == 'X < ' ):
        data =  ultimaDataNormalizada.replace('X < ','');

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        daysCalc  = campos[0];
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux - datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')

        
        return 'X < '  + retorno;

    else:
        data =  ultimaDataNormalizada;

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        daysCalc  = campos[0];
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux - datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        return retorno;
def __X_DAYS_EARLY      (found, listNorm):
    ultimaDataNormalizada = listNorm[len(listNorm)-1]
    if (ultimaDataNormalizada.find(' < X < ') != -1):
        datas = ultimaDataNormalizada.split(' < X < ');
        data1 = datas[0];
        data2 = datas[1];
        
        dia1 = data1.split('-')[0]; 
        mes1 = data1.split('-')[1]; 
        ano1 = data1.split('-')[2]; 
        
        dia2 = data2.split('-')[0]; 
        mes2 = data2.split('-')[1]; 
        ano2 = data2.split('-')[2];
        
        campos = found.split(' ');
        daysCalc  = campos[0];
        
        
        dataAux1 = datetime.date(ano1, mes1, dia1)
        dataAux2 = datetime.date(ano2, mes2, dia2)
        
        
        retorno1 = (dataAux1 - datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        retorno2 = (dataAux2 - datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        
        return retorno1 + ' < X < ' + retorno2;

    elif (ultimaDataNormalizada[:4] == 'X < ' ):
        data =  ultimaDataNormalizada.replace('X < ','');

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        daysCalc  = campos[0];
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux - datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')

        
        return 'X < '  + retorno;

    else:
        data =  ultimaDataNormalizada;

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        daysCalc  = campos[0];
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux - datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        return retorno;
def __X_DAYS_LATE       (found, listNorm):
    ultimaDataNormalizada = listNorm[len(listNorm)-1]
    if (ultimaDataNormalizada.find(' < X < ') != -1):
        datas = ultimaDataNormalizada.split(' < X < ');
        data1 = datas[0];
        data2 = datas[1];
        
        dia1 = data1.split('-')[0]; 
        mes1 = data1.split('-')[1]; 
        ano1 = data1.split('-')[2]; 
        
        dia2 = data2.split('-')[0]; 
        mes2 = data2.split('-')[1]; 
        ano2 = data2.split('-')[2];
        
        campos = found.split(' ');
        daysCalc  = campos[0];
        
        
        dataAux1 = datetime.date(ano1, mes1, dia1)
        dataAux2 = datetime.date(ano2, mes2, dia2)
        
        
        retorno1 = (dataAux1 + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        retorno2 = (dataAux2 + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        
        return retorno1 + ' < X < ' + retorno2;

    elif (ultimaDataNormalizada[:4] == 'X < ' ):
        data =  ultimaDataNormalizada.replace('X < ','');

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        daysCalc  = campos[0];
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')

        
        return 'X < '  + retorno;

    else:
        data =  ultimaDataNormalizada;

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        daysCalc  = campos[0];
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        return retorno;
def __X_DAYS_LATER      (found, listNorm):
    ultimaDataNormalizada = listNorm[len(listNorm)-1]
    if (ultimaDataNormalizada.find(' < X < ') != -1):
        datas = ultimaDataNormalizada.split(' < X < ');
        data1 = datas[0];
        data2 = datas[1];
        
        dia1 = data1.split('-')[0]; 
        mes1 = data1.split('-')[1]; 
        ano1 = data1.split('-')[2]; 
        
        dia2 = data2.split('-')[0]; 
        mes2 = data2.split('-')[1]; 
        ano2 = data2.split('-')[2];
        
        campos = found.split(' ');
        daysCalc  = campos[0];
        
        
        dataAux1 = datetime.date(ano1, mes1, dia1)
        dataAux2 = datetime.date(ano2, mes2, dia2)
        
        
        retorno1 = (dataAux1 + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        retorno2 = (dataAux2 + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        
        return retorno1 + ' < X < ' + retorno2;

    elif (ultimaDataNormalizada[:4] == 'X < ' ):
        data =  ultimaDataNormalizada.replace('X < ','');

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        daysCalc  = campos[0];
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')

        
        return 'X < '  + retorno;

    else:
        data =  ultimaDataNormalizada;

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        daysCalc  = campos[0];
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        return retorno;
def __X_DAYS_AFTER      (found, listNorm):
    ultimaDataNormalizada = listNorm[len(listNorm)-1]
    if (ultimaDataNormalizada.find(' < X < ') != -1):
        datas = ultimaDataNormalizada.split(' < X < ');
        data1 = datas[0];
        data2 = datas[1];
        
        dia1 = data1.split('-')[0]; 
        mes1 = data1.split('-')[1]; 
        ano1 = data1.split('-')[2]; 
        
        dia2 = data2.split('-')[0]; 
        mes2 = data2.split('-')[1]; 
        ano2 = data2.split('-')[2];
        
        campos = found.split(' ');
        daysCalc  = campos[0];
        
        
        dataAux1 = datetime.date(ano1, mes1, dia1)
        dataAux2 = datetime.date(ano2, mes2, dia2)
        
        
        retorno1 = (dataAux1 + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        retorno2 = (dataAux2 + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        
        return retorno1 + ' < X < ' + retorno2;

    elif (ultimaDataNormalizada[:4] == 'X < ' ):
        data =  ultimaDataNormalizada.replace('X < ','');

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        daysCalc  = campos[0];
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')

        
        return 'X < '  + retorno;

    else:
        data =  ultimaDataNormalizada;

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        daysCalc  = campos[0];
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        return retorno;
def __AFTER_X_DAYS      (found, listNorm):
    ultimaDataNormalizada = listNorm[len(listNorm)-1]
    if (ultimaDataNormalizada.find(' < X < ') != -1):
        datas = ultimaDataNormalizada.split(' < X < ');
        data1 = datas[0];
        data2 = datas[1];
        
        dia1 = data1.split('-')[0]; 
        mes1 = data1.split('-')[1]; 
        ano1 = data1.split('-')[2]; 
        
        dia2 = data2.split('-')[0]; 
        mes2 = data2.split('-')[1]; 
        ano2 = data2.split('-')[2];
        
        campos = found.split(' ');
        daysCalc  = campos[1];
        
        
        dataAux1 = datetime.date(ano1, mes1, dia1)
        dataAux2 = datetime.date(ano2, mes2, dia2)
        
        
        retorno1 = (dataAux1 + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        retorno2 = (dataAux2 + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        
        return retorno1 + ' < X < ' + retorno2;

    elif (ultimaDataNormalizada[:4] == 'X < ' ):
        data =  ultimaDataNormalizada.replace('X < ','');

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        daysCalc  = campos[1];
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')

        
        return 'X < '  + retorno;

    else:
        data =  ultimaDataNormalizada;

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        daysCalc  = campos[1];
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux + datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        return retorno;
def __BEFORE_X_DAYS     (found, listNorm):
    ultimaDataNormalizada = listNorm[len(listNorm)-1]
    if (ultimaDataNormalizada.find(' < X < ') != -1):
        datas = ultimaDataNormalizada.split(' < X < ');
        data1 = datas[0];
        data2 = datas[1];
        
        dia1 = data1.split('-')[0]; 
        mes1 = data1.split('-')[1]; 
        ano1 = data1.split('-')[2]; 
        
        dia2 = data2.split('-')[0]; 
        mes2 = data2.split('-')[1]; 
        ano2 = data2.split('-')[2];
        
        campos = found.split(' ');
        daysCalc  = campos[1];
        
        
        dataAux1 = datetime.date(ano1, mes1, dia1)
        dataAux2 = datetime.date(ano2, mes2, dia2)
        
        
        retorno1 = (dataAux1 - datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        retorno2 = (dataAux2 - datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        
        return retorno1 + ' < X < ' + retorno2;

    elif (ultimaDataNormalizada[:4] == 'X < ' ):
        data =  ultimaDataNormalizada.replace('X < ','');

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        daysCalc  = campos[1];
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux - datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')

        
        return 'X < '  + retorno;

    else:
        data =  ultimaDataNormalizada;

        data = datas[0];
        
        dia = data.split('-')[0]; 
        mes = data.split('-')[1]; 
        ano = data.split('-')[2]; 
        
        campos = found.split(' ');
        daysCalc  = campos[1];
        
        
        dataAux = datetime.date(ano, mes, dia)
        
        
        retorno = (dataAux - datetime.timedelta(days=daysCalc)).strftime('%d/%m/%Y')
        
        return retorno;
#20140416 - George Alves - FIM
#Retorna a expressão encontrada
def __ExpressionReturn(expression, text):
    reMDA = expression
    regMDA = re.compile(reMDA, re.IGNORECASE)
    found = regMDA.findall(text)
    return [a[0] for a in found if len(a) > 1]