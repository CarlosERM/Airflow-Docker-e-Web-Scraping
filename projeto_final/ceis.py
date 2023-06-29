# Empresas Inidôneas e Suspensas
# API CEIS: https://api.portaldatransparencia.gov.br/api-de-dados/ceis
# API ReceitaWS: https://receitaws.com.br/v1/cnpj/
# Fonte: https://portaldatransparencia.gov.br/download-de-dados/ceis

import os
from dotenv import load_dotenv
from pandas import DataFrame


class Ceis:
    def __init__(self):
        load_dotenv()
        self.headers = {
            "accept": "*/*",
            "chave-api-dados": os.environ.get("TOKEN"),
        }
        self.api_url_ceis = os.environ.get("API_URL_CEIS")
        self.api_url_ws = os.environ.get("API_URL_WS")
        self.api_url_google = os.environ.get("API_URL_GOOGLE")
        self.token_google = os.environ.get("TOKEN_GOOGLE")

    def isCPForCNPJValid(self, cpf_or_cnpj: str) -> bool:
        import re

        return re.match(
            r"([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})",
            cpf_or_cnpj,
        )

    def collect_data_ceis(self, cpf_or_cnpj: str) -> list:
        import requests

        response = requests.get(
            self.api_url_ceis,
            params={
                "codigoSancionado": cpf_or_cnpj,
                "pagina": "1",
            },
            headers=self.headers,
        )
        if response:
            company = response.json()
        else:
            company = response.json()
        return company

    def cleanCPF_CNPJ(self, cpf_or_cnpj) -> str:
        remove_chars: list[str] = [".", "/", "-"]
        for char in remove_chars:
            cpf_or_cnpj = cpf_or_cnpj.replace(char, "")
        return cpf_or_cnpj

    def import_companies(self, companies_path: str):
        import pandas as pd

        list_companies = pd.read_excel(companies_path)
        companies_array: list = []
        remove_chars: list[str] = [".", "/", "-"]

        for index, row in list_companies.iterrows():
            cpf_or_cnpj: str = row["CPF/CNPJ"]

            if self.isCPForCNPJValid(cpf_or_cnpj):
                cpf_or_cnpj = self.cleanCPF_CNPJ(cpf_or_cnpj)

                for company in self.collect_data_ceis(cpf_or_cnpj):
                    companies_array.append(company)
            else:
                print("deu errado")
        if len(companies_array) == 0:
            self.companies_df = []
            print("Não existem correspondências.")
        else:
            self.companies_df = pd.json_normalize(companies_array)

    def delete_not_wanted_columns(self, companies: DataFrame) -> None:
        companies.drop(
            [
                "id",
                "dataReferencia",
                "dataPublicacaoSancao",
                "dataTransitadoJulgado",
                "dataOrigemInformacao",
                "textoPublicacao",
                "linkPublicacao",
                "detalhamentoPublicacao",
                "numeroProcesso",
                "abrangenciaDefinidaDecisaoJudicial",
                "informacoesAdicionaisDoOrgaoSancionador",
                # "tipoSancao.descricaoResumida",
                "tipoSancao.descricaoPortal",
                "fonteSancao.nomeExibicao",
                "fonteSancao.telefoneContato",
                "fonteSancao.enderecoContato",
                "pessoa.id",
                "pessoa.cpfFormatado",
                "pessoa.cnpjFormatado",
                "pessoa.numeroInscricaoSocial",
                "pessoa.nome",
                "pessoa.razaoSocialReceita",
                "pessoa.nomeFantasiaReceita",
                "pessoa.tipo",
                "orgaoSancionador.poder",
                # "fundamentacao",
            ],
            axis=1,
            inplace=True,
        )

    def rename_columns(self, companies: DataFrame) -> None:
        companies.rename(
            columns={
                "dataInicioSancao": "data_inicio_sancao",
                "dataFimSancao": "data_fim_sancao",
                "orgaoSancionador.nome": "nome_orgao_sancionador",
                "orgaoSancionador.siglaUf": "uf_orgao_sancionador",
                "sancionado.nome": "nome_sancionado",
                "sancionado.codigoFormatado": "codigo_sancionado",
            },
            inplace=True,
        )

    def treat_companies_data(self):
        if len(self.companies_df) != 0:
            self.delete_not_wanted_columns(self.companies_df)
            self.rename_columns(self.companies_df)
        else:
            print("Não existem correspondências.")

    def is_CNPJ(self, cpf_or_cnpj: str) -> bool:
        import re

        return re.match(
            r"([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})",
            cpf_or_cnpj,
        )

    def get_lat_long(self, address_json):
        import requests

        address: str = f'{address_json["logradouro"]}, {address_json["bairro"]} {address_json["numero"]}, {address_json["municipio"]} {address_json["uf"]}'

        response = requests.get(
            self.api_url_google,
            params={
                "key": self.token_google,
                "address": address,
            },
        ).json()

        if response:
            location = response["results"][0]["geometry"]["location"]
            formatted_address = response["results"][0]["formatted_address"]
            lat = location["lat"]
            lng = location["lng"]
            return (formatted_address, lat, lng)
        else:
            return ()

    def get_company_location(self):
        import requests
        import pandas as pd
        import time

        result: DataFrame
        addresses: list = []
        if len(self.companies_df) != 0:
            for index, row in self.companies_df.iterrows():
                print(index)
                if index != 0 and index % 3 == 0:
                    time.sleep(60)
                cpf_or_cnpj: str = row["codigo_sancionado"]

                if self.is_CNPJ(cpf_or_cnpj):
                    cnpj: str = self.cleanCPF_CNPJ(cpf_or_cnpj)
                    response = requests.get(self.api_url_ws + cnpj)
                    if response.status_code == 429:
                        print("Espere 60 segundos...")
                        time.sleep(60)
                        pass
                    elif response.status_code == 200:
                        address_json = response.json()
                        address_lat_long = self.get_lat_long(address_json)

                        if len(address_lat_long) == 3:
                            addresses.append(
                                {
                                    "endereco": address_lat_long[0],
                                    "latitude": address_lat_long[1],
                                    "longitude": address_lat_long[2],
                                }
                            )
                        else:
                            addresses.append({})
                else:
                    addresses.append({})
                address_df = pd.DataFrame(data=addresses)
                result = pd.concat(
                    [self.companies_df, address_df], axis=1, join="inner"
                )
            result.to_csv("./teste_google_api.csv", index=False)
        else:
            print("Não existem correspondências.")


empresas_inidoneas: Ceis = Ceis()
empresas_inidoneas.import_companies("planilha_exemplo_2.xlsx")
empresas_inidoneas.treat_companies_data()
empresas_inidoneas.get_company_location()
