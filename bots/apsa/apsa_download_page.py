from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.utils import wait_for_new_file, get_downloaded_files
import time


class ApsaDownloadPage:
    def __init__(self, driver):
        self.driver = driver
        self.url_boleto = "https://areaexclusiva.apsa.com.br/digital/cotas/visualizacaoIndividual"
        self.listagem_boletos_locator = (By.XPATH, "/html/body/app-root/ion-app/ion-router-outlet/app-layout/ion-app/div[2]/section/ion-router-outlet/app-index/ion-content/app-list-cotas/div/div[4]")
        self.lista_items_locator = (By.CLASS_NAME, "Item_DetalhamentoCota_Item")
        self.valor_locator = (By.XPATH, ".//div[contains(@class, 'Label') and text()='Devido:']/following-sibling::div[contains(@class, 'Highlighted')]")
        self.vencimento_locator = (By.XPATH, ".//div[contains(@class, 'Label') and text()='Vencimento:']/following-sibling::div[contains(@class, 'Highlighted')]")
        self.situacao_locator = (By.XPATH, ".//div[contains(@class, 'Label') and text()='Situação']/following-sibling::div[contains(@class, 'Highlighted')]")
        self.btn_2a_via_locator = (By.XPATH, ".//div[contains(@class, 'Actions_Option_Label') and contains(text(), 'Emitir 2ª via')]")

    def listagem_boleto(self):
        try:
            wait = WebDriverWait(self.driver, 20)
            time.sleep(5)
            self.driver.get(self.url_boleto)
            listagem_boletos_e = wait.until(EC.visibility_of_element_located(self.lista_items_locator))
            if listagem_boletos_e:
                print("Entrou na listagem de Boletos.")
                return True
        except Exception as e:
            print(f"Não conseguiu chegar na listagem de Boletos. Erro: {e}")
            return False

    def get_info_boleto(self):

        try:
            wait = WebDriverWait(self.driver, 20)
            time.sleep(2)
            lista_items_e = wait.until(EC.presence_of_all_elements_located(self.lista_items_locator))
            boletos_info = []

            download_dir = r"C:\Users\Jose\Documents\GitHub\administramosImoveis\bots\apsa\downloads"
            previous_files = get_downloaded_files(download_dir)

            for item in lista_items_e:
                valor_e = item.find_element(*self.valor_locator)
                valor = valor_e.text.strip()            

                vencimento_element = item.find_element(*self.vencimento_locator)
                vencimento = vencimento_element.text.strip()

                situacao_element = item.find_element(*self.situacao_locator)
                situacao = situacao_element.text.strip()                

                if situacao.lower() == "em aberto":
                    
                    boletos_info.append({
                        'vencimento': vencimento,
                        'valor': valor,
                        'situacao': situacao,
                        'download_concluido': False
                    })

                    botao_2a_via = item.find_element(*self.btn_2a_via_locator)
                    botao_2a_via.click()
                    print("Clicou no botão de Emitir 2ª via.")

                    try:
                        new_file = wait_for_new_file(download_dir, previous_files)
                        print(f"Novo arquivo baixado: {new_file}.")
                        boletos_info[-1]['download_concluido'] = True
                    except TimeoutError:
                        print("O download do arquivo excedeu o tempo limite.")
                        boletos_info[-1]['download_concluido'] = False

            return boletos_info

        except Exception as e:
            print(f"Erro ao buscar informações dos boletos: {e}")
            return False