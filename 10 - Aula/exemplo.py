from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class Principal(webdriver.Chrome):
    def __init__(self):
        options = webdriver.ChromeOptions().add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service(ChromeDriverManager().install())
        super(Principal, self).__init__(service=service, options=options)
        self.maximize_window()
    def abrirFace(self):
        self.get('https://www.facebook.com')
        print("O Título da página é: ", self.title)
        print("O endereço URL é: ", self.current_url)
        time.sleep(3)

if __name__ == "__main__":
    bot = Principal()
    bot.abrirFace()
