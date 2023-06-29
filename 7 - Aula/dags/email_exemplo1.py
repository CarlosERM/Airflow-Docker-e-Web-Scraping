# Aluno: Carlos Eduardo Rocha Miranda
# Professor: Jesmmer.
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import timedelta, datetime


def primeira_funcao():
    print("Primeira função está funcionando.")


def on_failure_callback():
    print("Deu muito ruim.")


email_exemplo1 = DAG(
    dag_id="email_exemplo1",
    schedule_interval='@once',
    default_args={
                      "owner": "airflow",
                      "start_date": datetime(2023, 3, 16),
                      "retries": 1,
                      "retry_delay": timedelta(minutes=1),
                      "on_failure_callback": on_failure_callback,
                      'email': ['carlos.eduardo@estudante.ifgoiano.edu.br'],
                      'email_on_failure': False,
                      'email_on_retry': False,
    },
    description="Essa dag vai mandar um email pras outras pessoas.",
    start_date=datetime(2023, 1, 1),
    catchup=False)

primeira_funcao = PythonOperator(
    task_id="primeira_funcao",
    python_callable=primeira_funcao,
    dag=email_exemplo1,
)
send_email = EmailOperator(
    task_id='enviar_email',
    to='carlos.eduardo@estudante.ifgoiano.edu.br',
    subject='Alerta do Airflow',
    html_content="""<h3> Teste de Email do Airflow. Data {{ ds }}</h3>""",
    dag=email_exemplo1)

primeira_funcao >> send_email
