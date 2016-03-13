# coding: utf-8
import sys
import re
from xml.dom.minidom import parseString
import datetime
import os
from os.path import basename
import RISOTemportalTaggerNormalization
import psycopg2
from ctypes.test.test_values import ValuesTestCase

class RisoTemporalTagger:
    """ Analisa um texto de input a procura de expressoes temporais. As expressoes temporais sao
        lidas a partir de um arquivo de configuracao.
    """
    def __init__(self, path_configuracao="config.xml"):
        """ Inicializa o analisador. Recebe o path para o arquivo de configuracao a ser lido.
        """
        self.patterns = {} #Strings
        self.patterns_regex = {} #SRE_Pattern
        self.rules = {} #[Strings]
        self.rule_names = {} #Strings
        self.normList = [] # 20140415 - George Alves
        
        data = self.__read_file(path_configuracao)

        #Ordem eh importante - Sempre comecar pelos terminais
        self.__load_patterns(data)
        self.__load_rules(data) #Faz a leitura do arquivo e carrega todas as expressoes
    
    def __read_file(self, path):
        """ Abre o arquivo do 'path' e retorna todo o seu conteudo.
        """
        try:
            file = open(path, 'r')
            data = file.read()
            file.close()
            return data
        except:
            print "Arquivo " + path + " nao encontrado."
            sys.exit(-1)

    def __load_rules(self, data):
        """ Recebe os dados de configuracao em uma string XML e carrega todas as regras.
            self.rules dict -> list[string]
        """
        config_dom = parseString(data)
        rules_xml = config_dom.getElementsByTagName('regra')
        for tag in rules_xml:
            rule_filepath = tag.getAttribute('arquivo')
            xml = parseString(self.__read_file(rule_filepath))
            rules_list = xml.getElementsByTagName('simbolo')
            for rule in rules_list:
                symbol = rule.getAttribute('nome')
                expression = rule.getElementsByTagName('expressao')
                sub_expression = []
                for exp in expression:
                    rule_body = exp.firstChild.data
                    sub_expression.append(rule_body)
                    self.rule_names[rule_body] = exp.getAttribute('tipo').encode('ascii') #gambiarra
                self.rules[symbol] = sub_expression
        
    def __load_patterns(self, data):
        """ Recebe os dados de configuracao em uma string XML e carrega todos os padroes.
            self.patterns dict -> regex(string)
        """
        config_dom = parseString(data)
        pattern_xml = config_dom.getElementsByTagName('padrao')
        for tag in pattern_xml:
            pattern_filepath = tag.getAttribute('arquivo')
            print tag.getAttribute('arquivo')
            if (tag.getAttribute('arquivo') == 'C:/Users/george.marcelo.alves/git/RisoTemporalTagger_master/RisoTemporalTagger_master/padroes/datas_especiais.xml'):
                print
            xml = parseString(self.__read_file(pattern_filepath))
            pattern = xml.getElementsByTagName('simbolo')[0] # um padrao por arquivo
            symbol = pattern.getAttribute('nome')
            expressions = pattern.getElementsByTagName('expressao')
            pattern_values = r""
            for exp in expressions:
                pattern_values += exp.firstChild.data[1:-1] + "|"
            
            #Retira o ultimo "|" do final da regex
            pattern_values = pattern_values[:len(pattern_values)-1] 
            self.patterns[symbol] = pattern_values
            self.patterns_regex[symbol] = re.compile(pattern_values)
         
    def __identifier(self, scanner, token): return "ID", token
    def __string(self, scanner, token):   return "STRING", token
    def __blank_space(self, scanner, token): return "ESPACO", token
    def __generate_tokens(self, input):
        """ Realiza a analise lexica das expressoes da gramatica fornecida.
        """
        scanner = re.Scanner([(r"[a-zA-Z_]\w*", self.__identifier),(r'\".*?\"', self.__string), (r"\s+", self.__blank_space)])
        tokens, remainder = scanner.scan(input)
        return tokens
    
    def __try_any_match(self, symbol, input_position):
        """ Recebe um simbolo da gramatica e tenta fazer um match.
            
            OBS: Limite da pilha de recursao eh 1000 (limitacao do Python). Se precisar aumentar, 
            ha um metodo na lib "sys" que aparentemente permite fazer isso.
        """
        #Carrega expressoes do simbolo
        expressions = None
        if (symbol in self.rules):
            expressions = self.rules[symbol]
        else:
            print "SIMBOLO \"" + symbol + "\" NaO FOI DEFINIDO"
            sys.exit(-1)
            
        #Processa a regra
        local_position = input_position

        expressions = sorted(expressions, key= lambda aux: len(self.__generate_tokens(aux)), reverse = True)

        retorno1 = ""
        retorno2 = ""               
        for exp in expressions:
            local_position = input_position # george teste
            value = ""
            tokens = self.__generate_tokens(exp)
            exp_sucess = True
            for token in tokens:
                regex = None
                match = None
                if (token[0] == "ID"):
                    #Se for um padrao, tenta fazer o match
                    if (self.patterns.get(token[1]) is not None):
                        regex = re.compile(self.patterns[token[1]], self.__flags) #Retira as aspas
                        match = regex.match(self.__input, local_position)
                    else:
                        rule_matched, sub_value = self.__try_any_match(token[1], local_position)
                        match = None if sub_value is None else sub_value
                elif (token[0] == "STRING"):
                    regex = re.compile(token[1][1:-1], self.__flags) #Retira as aspas
                    match = regex.match(self.__input, local_position)
                else: #Espacos em branco
                    regex = re.compile(token[1], self.__flags)
                    match = regex.match(self.__input, local_position)
                
                if match is None: 
                    local_position = input_position
                    exp_sucess = False
                    break
                else:
                    if type(match) == str:
                        value += match
                        local_position += len(value) 
                    else:
                        value += match.group()
                        local_position = match.end()
                
            if exp_sucess:
                if (len(value) > len(retorno2) ):
                    retorno2 = value
                    retorno1 = self.rule_names.get(exp) 
                #return self.rule_names.get(exp), value
        if (len(retorno2) > 0):
            return retorno1, retorno2
        return None, None 

    def list(self, path, case_sensitive=False, rule="expressao_temporal"):
        """ Retorna a lista de expressoes encontradas no arquivo 'path' utilizando a gramatica 
            configurada.
            Ex: conteudo do arquivo = 'since he left on jan 1 , 1988' 
                                   -> ['since','on jan 1 , 1988']
        """
        self.__input = self.__read_file(path)
        self.__position = 0
        
        if case_sensitive:
            self.__flags = re.M
        else:
            self.__flags = re.M|re.I
        
        matched_list = []
        while self.__position <= len(self.__input):
            rule_matched, value_matched = self.__try_any_match(rule, self.__position)
            if value_matched is None:
                self.__position += 1
            else:
                print str(rule_matched) + " -> " + str(value_matched)
                matched_list.append(value_matched)
                self.__position += len(value_matched)
        return matched_list
        
    def tag(self, path, case_sensitive=False, rule="expressao_temporal"):
        """ Retorna o texto do arquivo 'path' marcado com as expressoes encontradas utilizando a 
            gramatica configurada.
            Ex: conteudo do arquivo = 'since he left on jan 1 , 1988' 
                                   -> '<tag>since</tag> he left <tag>on jan 1 , 1988</tag>'
        """
        self.__input = self.__read_file(path)
        self.__position = 0
        
        if case_sensitive:
            self.__flags = re.M
        else:
            self.__flags = re.M|re.I
        
        tagged_text = ""
        while self.__position < len(self.__input):
            rule_matched, value_matched = self.__try_any_match(rule, self.__position)
            if value_matched is None:
                tagged_text += self.__input[self.__position]
                self.__position += 1
            else:
                tagged_text += "<RISOTime type=" + rule_matched + ">" + value_matched + "</RISOTime>"
                self.__position += len(value_matched)
        return tagged_text
    def normalization(self, path, case_sensitive=False, rule="expressao_temporal"):
        self.__input = self.__read_file(path)
        self.__position = 0
        
        nomeDocumento = basename(path)
        documentId = self.__INSERT_DOCUMENT_INFO(nomeDocumento)

        if case_sensitive:
            self.__flags = re.M
        else:
            self.__flags = re.M|re.I

        normalizacaoAnterior = ""
        while self.__position <= len(self.__input):
            rule_matched, value_matched = self.__try_any_match(rule, self.__position)
            if value_matched is None:
                self.__position += 1
            else:
                # george remover
                # print(value_matched)
                normalizacao = str(self.__dateNormalization(rule_matched, value_matched))
                print str(value_matched) + " <--> " + normalizacao
                
                if (("mapeado" not in normalizacao) and (normalizacao <> "")):
                    self.__INSERT_DATA_NORM(value_matched, normalizacao, documentId)
                self.__position += len(value_matched)
                
                self.normList.append(normalizacao) # 20140415 - George Alves

    def ExpressionReturn(self, expression, text):
        reMDA = expression
        regMDA = re.compile(reMDA, re.IGNORECASE)
        found = regMDA.findall(text)
        result = ""
        for a in found:
            if len(a) > 1:
                result = result + a[0]
        
        return [a[0] for a in found if len(a) > 1]
    def __INSERT_DATA_NORM (self, data, dataNorm, idDocumento):
        qtdNum = "([0-9]+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|twenty-one|twenty-two|twenty-three|twenty-four|twenty-five|twenty-six|twenty-seven|twenty-eight|twenty-nine|thirty|thirty-one|thirty-two|thirty-three|thirty-four|thirty-five|thirty-six|thirty-seven|thirty-eight|thirty-nine|forty|forty-one|forty-two|forty-three|forty-four|forty-five|forty-six|forty-seven|forty-eight|forty-nine|fifty|fifty-one|fifty-two|fifty-three|fifty-four|fifty-five|fifty-six|fifty-seven|fifty-eight|fifty-nine|sixty|sixty-one|sixty-two|sixty-three|sixty-four|sixty-five|sixty-six|sixty-seven|sixty-eight|sixty-nine|seventy|seventy-one|seventy-two|seventy-three|seventy-four|seventy-five|seventy-six|seventy-seven|seventy-eight|seventy-nine|eighty|eighty-one|eighty-two|eighty-three|eighty-four|eighty-five|eighty-six|eighty-seven|eighty-eight|eighty-nine|ninety|ninety-one|ninety-two|ninety-three|ninety-four|ninety-five|ninety-six|ninety-seven|ninety-eight|ninety-nine|a hundred|one hundred|a thousand|one thousand)" #20140415 - George Alves

        __X_YEARS_BEFORE_EX = "^("+qtdNum+" year[s]* before)$"
        __X_YEARS_EARLY_EX  = "^("+qtdNum+" year[s]* early)$"
        __X_YEARS_EARLIER_EX  = "^("+qtdNum+" year[s]* earlier)$"
        __X_YEARS_LATE_EX   = "^("+qtdNum+" year[s]* late)$"
        __X_YEARS_LATER_EX  = "^("+qtdNum+" year[s]* later)$"
        __X_YEARS_AFTER_EX  = "^("+qtdNum+" year[s]* after)$"
        __AFTER_X_YEARS_EX  = "^(after "+qtdNum+" year[s]*)$"
        __BEFORE_X_YEARS_EX = "^(before "+qtdNum+" year[s]*)$"
        
        __BEFORE_X_YEARS_EX = "^(before "+qtdNum+" year[s]*)$"

        
        __X_MONTHS_BEFORE_EX = "^("+qtdNum+" month[s]* before)$"
        __X_MONTHS_EARLY_EX  = "^("+qtdNum+" month[s]* early)$"
        __X_MONTHS_EARLIER_EX  = "^("+qtdNum+" month[s]* earlier)$"
        __X_MONTHS_LATE_EX   = "^("+qtdNum+" month[s]* late)$"
        __X_MONTHS_LATER_EX  = "^("+qtdNum+" month[s]* later)$"
        __X_MONTHS_AFTER_EX  = "^("+qtdNum+" month[s]* after)$"
        __AFTER_X_MONTHS_EX  = "^(after "+qtdNum+" month[s]*)$"
        __BEFORE_X_MONTHS_EX = "^(before "+qtdNum+" month[s]*)$"
        
        __X_DAYS_BEFORE_EX = "^("+qtdNum+" day[s]* before)$"
        __X_DAYS_EARLY_EX  = "^("+qtdNum+" day[s]* early)$"
        __X_DAYS_LATE_EX   = "^("+qtdNum+" day[s]* late)$"
        __X_DAYS_LATER_EX  = "^("+qtdNum+" day[s]* later)$"
        __X_DAYS_AFTER_EX  = "^("+qtdNum+" day[s]* after)$"
        __AFTER_X_DAYS_EX  = "^(after "+qtdNum+" day[s]*)$"
        __BEFORE_X_DAYS_EX = "^(before "+qtdNum+" day[s]*)$"
        
        try:
            conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='postgres'")
            cur = conn.cursor()
            achou = False
            arrayFromEx = [__X_YEARS_BEFORE_EX, __X_YEARS_EARLY_EX, __X_YEARS_EARLIER_EX, __X_YEARS_LATE_EX, __X_YEARS_LATER_EX, __X_YEARS_AFTER_EX, __AFTER_X_YEARS_EX, __BEFORE_X_YEARS_EX, __X_MONTHS_BEFORE_EX, __X_MONTHS_EARLY_EX, __X_MONTHS_EARLIER_EX, __X_MONTHS_LATE_EX, __X_MONTHS_LATER_EX, __X_MONTHS_AFTER_EX, __AFTER_X_MONTHS_EX, __BEFORE_X_MONTHS_EX, __X_DAYS_BEFORE_EX, __X_DAYS_EARLY_EX, __X_DAYS_LATE_EX, __X_DAYS_LATER_EX, __X_DAYS_AFTER_EX, __AFTER_X_DAYS_EX, __BEFORE_X_DAYS_EX] 
            #20140415 - George Alves- Inclusao dos novos padroes - FIM 
            for regex in arrayFromEx:
                list = self.ExpressionReturn(regex, data)
                        
                if len(list) > 0:
                    achou = True
            
            if not (achou):
                #cur.execute("""  SELECT dn.* from datanorm dn where dn.data = '"""+str(data)+"""' """)
                #rows = cur.fetchall()
            
                foiInserido = False
                #for row in rows:
                #    foiInserido = True
            
                if (not foiInserido):
                    cur = conn.cursor()
                    dataInfo = ({"data":str(data), "datanormalizada":str(dataNorm)})            
                    cur.execute("""  insert into datanorm (id_documento, data, datanormalizada, seq_frase) values (""" +str(idDocumento)+ """, '""" +data+ """', '"""+dataNorm+"""', nextval('id_frase_seq')) """)
                    conn.commit()
                    
                    #cur.executemany("""INSERT INTO datanorm (data, datanomalizada) values  ('oi', 'oi')""")
    
                    # print """  INSERT INTO datanorm (data, datanormalizada) values ('"""+str(data)+"""', '"""+str(dataNorm)+"""')  """
                    # cur.executemany("""  INSERT INTO datanorm (data, datanomalizada) values (%(data)s, %(datanormalizada)s) ""--", dataInfo)
            else:
                #cur.execute("""  SELECT dn.* from datanorm dn where dn.data = '"""+str(data)+"""' """)
                #rows = cur.fetchall()
            
                foiInserido = False
                #for row in rows:
                #    foiInserido = True
            
                if (not foiInserido):
                    cur = conn.cursor()
                    dataInfo = ({"data":str(data), "datanormalizada":str(dataNorm)})            
                    cur.execute("""  insert into datanorm (id_documento, data, datanormalizada, seq_frase) values (""" +str(idDocumento)+ """, '""" +data+ """', '"""+dataNorm+"""', nextval('id_frase_seq')) """)
                    conn.commit()
                    
                    #cur.executemany("""INSERT INTO datanorm (data, datanomalizada) values  ('oi', 'oi')""")
    
                    # print """  INSERT INTO datanorm (data, datanormalizada) values ('"""+str(data)+"""', '"""+str(dataNorm)+"""')  """
                    # cur.executemany("""  INSERT INTO datanorm (data, datanomalizada) values (%(data)s, %(datanormalizada)s) ""--", dataInfo)
                
        except:
            print "I am unable to connect to the database"    

    def __INSERT_DOCUMENT_INFO (self, nomeDocumento):
        
        try:
            conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='postgres'")
            cur = conn.cursor()
            achou = False
            if not (achou):
                cur.execute("""  SELECT di.id_documento from documentinfo di where di.nome_documento = '"""+str(nomeDocumento)+"""' """)
                rows = cur.fetchall()
            
                foiInserido = False
                for row in rows:
                    retorno = row[0]
                    foiInserido = True
            
                if (not foiInserido):
                    cur = conn.cursor()
                    cur.execute("""  SELECT nextval('id_document_seq') """)
                    rows = cur.fetchall()
                
                    foiInserido = False
                    for row in rows:
                        retorno = row[0]
                    
                    
                    cur = conn.cursor()
                    cur.execute("""  insert into documentinfo (id_documento, nome_documento) values (""" +str(retorno)+ """, '"""+nomeDocumento+"""') """)
                    conn.commit()
                    
                return retorno
                    
                
        except:
            print "I am unable to connect to the database"    

    def __dateNormalization(self, rule_matched, value_matched):
        if rule_matched == 'EBT':
            
            #20150421 - George Alves - Alteracao para pegar datas anteriores na normalizacao - Inicio 
            retorno = RISOTemportalTaggerNormalization.Normalization(value_matched,rule_matched)
            
            if ("mapeado" in retorno):
                retorno = RISOTemportalTaggerNormalization.NormalizationListAnteriores(value_matched, self.normList, rule_matched)
            else:
                return retorno    
                
            return retorno
            #20150421 - George Alves - Alteracao para pegar datas anteriores na normalizacao - Fim
        
        elif rule_matched == 'EMT':
            return RISOTemportalTaggerNormalization.Normalization(value_matched,rule_matched)
        elif rule_matched == 'Pre-EMT':
            return RISOTemportalTaggerNormalization.Normalization(value_matched,rule_matched)
        elif rule_matched == 'Pre-A-Pre-A':
            return RISOTemportalTaggerNormalization.Normalization(value_matched,rule_matched)
        elif rule_matched == 'Pre-EBT':
            retorno = ''
            retorno =  RISOTemportalTaggerNormalization.Normalization(value_matched,rule_matched)
            if ("mapeado" in retorno):
                retorno = RISOTemportalTaggerNormalization.NormalizationListAnteriores(value_matched, self.normList, rule_matched)
            else:
                return retorno
                
            return retorno
        elif rule_matched == 'I':
            return RISOTemportalTaggerNormalization.Normalization(value_matched,rule_matched)		
        #20140416 - George Alves - INICIO 
        elif rule_matched == 'D-EMT-Adv':
            return RISOTemportalTaggerNormalization.NormalizationListAnteriores(value_matched, self.normList, rule_matched)        
        elif rule_matched == 'Adv-DE':
            return RISOTemportalTaggerNormalization.NormalizationDateInExpression(value_matched,rule_matched)        
        elif rule_matched == 'DE':
            return RISOTemportalTaggerNormalization.NormalizationDateInExpression(value_matched,rule_matched)        
        #20140416 - George Alves - FIM 
        else:
            return 'Padrão ' + rule_matched + ' ainda não foi mapeado'