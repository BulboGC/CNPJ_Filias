from selenium import webdriver
from openpyxl import Workbook
from tqdm import tqdm
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import time 


class Scrap:
    def __init__(self):
        self.DATABASE = []
        self.SITE_LINK = "https://cnpj.linkana.com"
        #********************* CNPJs QUE VAI PROCURAR COLOCAR NESSA LISTA*********************************
        #*********************VVVVVVVVVVVVVVVVVVVVVV**********************************
        self.SITE_LIST_CNPJ = ['45.242.914/0001-05']
        self.SITE_PATH_ARQUIVO_CSV = 'G:\\python scrapy\\'
        self.SITE_MAP = {
            'dados':{
                'cnpj':{'xpath':'/html/body/div/div/main/div[2]/div[1]/div/h2[2]/b[2]'},
                'razao_social':{'xpath':'/html/body/div/div/main/div[2]/ul[1]/li[1]/p'},
                'situacao':{'xpath':'/html/body/div/div/main/div[2]/ul[1]/li[3]/p'},
                'cep':{'xpath':'/html/body/div/div/main/div[2]/ul[2]/li[1]/p'},
                'endereco':{'xpath':'/html/body/div/div/main/div[2]/ul[2]/li[2]/div/p[2]'},
                'cidade':{'xpath':'/html/body/div/div/main/div[2]/ul[2]/li[3]/div[1]/p[2]'},
                'estado':{'xpath':'/html/body/div/div/main/div[2]/ul[2]/li[3]/div[2]/p'},
                'email':{'xpath':'VOUPEGAR'},
                'telefone':{'xpath': '/html/body/div/div/main/div[2]/ul[2]/li[5]/p'}
        },
            'elements':{'ul':{'xpath':'/html/body/div/div/main/div[2]/div[5]/ul/li[$$NUMBER$$]/a'}},
            'buttons':{
                'Mostrar_mais':{'xpath':'//*[@id="app"]/div/main/div[2]/div[5]/button'},
                'Entrar':{'xpath':'/html/body/div/div/main/div/div/a/div/div[1]/p[1]'},
                'pesquisar':{'xpath':'/html/body/div/div/main/div/div[1]/div/div[2]/form/div/button'},}}
       
        option = Options()
        option.headless = True
        self.browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=option)
        self.browser.maximize_window()
       
    
    def OpenLink(self,link):
        self.browser.get(link)
        time.sleep(1)

    def PesquisarCNPJ(self,nome_ou_cnpj):
        self.browser.find_element(by='xpath',value='/html/body/div/div/main/div/div[1]/div/div[2]/form/div/input').send_keys(nome_ou_cnpj)
        time.sleep(3)

    def Clicar(self,element):
        self.browser.find_element(by='xpath',value= element).click()
        time.sleep(5)

    def ClicarRapido(self,element):
        self.browser.find_element(by='xpath',value= element).click()
        time.sleep(0.5)

    def Coletar_Content_value(self,valor):
        return self.browser.find_element(by='xpath',value=valor).text

    def Coletar_dado(self,valor,atributo):
        
        return self.browser.find_element(by='xpath',value=valor).get_attribute(atributo)
    
    def Loop_coleta_links(self):       
        i = 1
        arr = []
        while True:
            try:
                dado = self.Coletar_dado(Firefox.SITE_MAP['elements']['ul']['xpath'].replace("$$NUMBER$$",str(i)),'href')
                arr.append(dado)
                i = i + 1
            except:
                break
        return arr
    
    def Loop_clique(self,value):
        index = 1
        while True:
            try:
        
                self.ClicarRapido(value)
                index = index + 1
            except:
                break 

    def Importar_cabecalho_csv(self,path_arquivo,nome_arquivo,dados):

        path = path_arquivo + nome_arquivo
        cabecalhos = []
        with open(path, 'w+') as arquivo:
            for linha in dados[0]:
                cabecalhos.append(linha)
                arquivo.write(str(linha)+';')
            arquivo.write('\n')
        return cabecalhos

    def Importar_dados_csv(self,path_arquivo,nome_arquivo,dados,cabecalhos):
        path = path_arquivo + nome_arquivo
        with open(path, 'a+') as arquivo:
            for key in tqdm(dados,'importando para o excel...'):
                i = 1
                for indice in cabecalhos:           
           
           
                    if i == len(cabecalhos):
                        arquivo.write(key[indice] + '\n')
                    else:
                        arquivo.write(key[indice] + ';')
                    i = i + 1


            
Firefox = Scrap()

for CNPJ in tqdm(Firefox.SITE_LIST_CNPJ,'Lojas ja pegadas'):

    Firefox.OpenLink(Firefox.SITE_LINK)
    Firefox.PesquisarCNPJ(CNPJ)
    Firefox.Clicar(Firefox.SITE_MAP['buttons']['pesquisar']['xpath'])
    Firefox.Clicar(Firefox.SITE_MAP['buttons']['Entrar']['xpath'])
    Firefox.Loop_clique(Firefox.SITE_MAP['buttons']['Mostrar_mais']['xpath'])
    list = Firefox.Loop_coleta_links()
   

    for link in tqdm(list,'obtendo dados para importação'):
        Firefox.OpenLink(link)
        obj = {}
        obj['razao_social'] = Firefox.Coletar_Content_value(Firefox.SITE_MAP['dados']['razao_social']['xpath']) 
        obj['situacao'] = Firefox.Coletar_Content_value(Firefox.SITE_MAP['dados']['situacao']['xpath'])
        obj['link'] = link
        obj['cnpj'] = Firefox.Coletar_Content_value(Firefox.SITE_MAP['dados']['cnpj']['xpath'])    
        Firefox.DATABASE.append(obj)
  
    c = 0
    if c == 0: 
        
        cabecalhos = Firefox.Importar_cabecalho_csv(Firefox.SITE_PATH_ARQUIVO_CSV,'Dados.csv',Firefox.DATABASE)
        c = 1
    

    Firefox.Importar_dados_csv(Firefox.SITE_PATH_ARQUIVO_CSV,'Dados.csv',Firefox.DATABASE,cabecalhos)
        







 
Firefox.browser.close()




