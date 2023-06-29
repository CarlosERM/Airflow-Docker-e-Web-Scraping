import json
import pathlib
import airflow.utils.dates
import requests
import requests.exceptions as requests_exceptions
from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

dag = DAG(dag_id="exemplo_4_launch",
          description="Baixar imagens de lançamentos de foguetes", start_date=airflow.utils.dates.days_ago(14),
          schedule_interval="@daily",)

download_lancamentos = BashOperator(
    task_id="download_lancamentos", bash_command="curl -o /tmp/launches.json -L 'https://ll.thespacedevs.com/2.0.0/launch/upcoming'",
    dag=dag)


def pegar_imagens():
    pathlib.Path("/tmp/images").mkdir(parents=True, exist_ok=True)
    with open("/tmp/launches.json") as f:
        launches = json.load(f)
        image_urls = [launch["image"] for launch in launches["results"]]
        for image_url in image_urls:
            try:
                response = requests.get(image_url)
                image_filename = image_url.split("/")[-1]
                target_file = f"/tmp/images/{image_filename}"
                with open(target_file, "wb") as f:
                    f.write(response.content)
                print(f"Imagem {image_url} baixada em {target_file}")
            except requests_exceptions.MissingSchema:
                print(f"{image_url} deve estar com URL inválido.")
            except requests_exceptions.ConnectionError:
                print(f"Não foi possível conectar com {image_url}.")


pegar_imagens = PythonOperator(
    task_id="pegar_imagens",
    python_callable=pegar_imagens,
    dag=dag
)

notificar = BashOperator(
    task_id="notificar",
    bash_command='echo "Existem $(ls /tmp/images/ | wc -l) imagens."',
    dag=dag)

download_lancamentos >> pegar_imagens >> notificar
