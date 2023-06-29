from datetime import datetime
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import BranchPythonOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

dag = DAG(dag_id="exemplo_1_branching", description="Exemplo de dag com branching",
          start_date=datetime(2023, 3, 4), schedule_interval="@daily")


def _verifica_valor():
    valor = int(Variable.get("valor"))
    if valor >= 10:
        return "maior_ou_igual_a_10"
    else:
        return "menor_10"


def _finalizar():
    print("Fim da DAG.")


verifica = BranchPythonOperator(
    task_id="verificar",
    python_callable=_verifica_valor,
    dag=dag
)


maiorIgual = EmptyOperator(
    task_id="maior_ou_igual_a_10",
    dag=dag
)

menor = EmptyOperator(task_id="menor_10", dag=dag)

finalizar = PythonOperator(
    task_id="finalizar", python_callable=_finalizar, dag=dag)


verifica >> [maiorIgual, menor]
maiorIgual >> finalizar
