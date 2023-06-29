# Aluno: Carlos Eduardo Rocha Miranda
# Professor: Jesmmer.
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import timedelta, datetime
from airflow.operators.email import send_email
from airflow.utils.state import State
DAG_NAME = 'email_exemplo2'
default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 3, 16),
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
    'email': ['carlos.eduardo@estudante.ifgoiano.edu.br'],
    'email_on_failure': True,
}


def _email_confirmacao(kwargs):
    dag_run = kwargs['dag_run']
    email = 'carlos.eduardo@estudante.ifgoiano.edu.br',
    title = ''
    body = ''

    if dag_run._state == State.SUCCESS:
        dateTimeReport = datetime.now()

        title = f"Alerta Airflow: {dag_run.dag_id} confirmada -{dateTimeReport.strftime('%d-%b%Y (%H:%M)')}-"
        body = """
        Olá! Bom dia!, 
        <br>Dag {dag_id} foi executada com sucesso!</br>
        <br>Atenciosamente, Bot Airflow.</br>
        """.format(dag_id=dag_run.dag_id)
    send_email(email, title, body)


email_exemplo1 = DAG(
    dag_id=f'{DAG_NAME}',
    default_args=default_args,
    schedule_interval='@once',
    on_success_callback=_email_confirmacao,
    description="Essa dag vai mandar um email pras outras pessoas.",
    start_date=datetime(2023, 1, 1),
    catchup=False)

enviar_email_jesmmer = EmailOperator(
    task_id='enviar_email',
    to='jesmmer.alves@ifgoiano.edu.br',
    subject=f"Airflow",
    html_content="""<h3>Melhor professor!!!!</h3>""",
    dag=email_exemplo1)

enviar_email_jesmmer
