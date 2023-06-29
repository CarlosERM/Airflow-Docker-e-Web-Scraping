import json
import airflow.utils.dates
from airflow import DAG
from airflow.operators.python import BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

dag = DAG(dag_id="atividade_2",
          description="Pega os dados de New York", start_date=airflow.utils.dates.days_ago(1),
          schedule_interval="@daily",)

captura_conta_dados = BashOperator(
    task_id="captura_conta_dados",
    bash_command="curl -o /tmp/city_of_new_york.json -L 'https://data.cityofnewyork.us/resource/rc75-m7u3.json'",
    dag=dag)


def e_valida():
    with open("/tmp/city_of_new_york.json") as f:
        data = json.load(f)
        if len(data) > 10:
            return "valido"
        else:
            return "invalido"


e_valida = BranchPythonOperator(
    task_id="e_valida",
    python_callable=e_valida,
    dag=dag)

invalido = EmptyOperator(
    task_id="invalido",
    dag=dag)

valido = EmptyOperator(
    task_id="valido",
    dag=dag)


captura_conta_dados >> e_valida >> [invalido, valido]
