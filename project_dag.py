from datetime import timedelta,datetime
from airflow.operators.empty import EmptyOperator
from airflow import DAG
from airflow.operators.python import PythonOperator
from DemoCovidProject.clonefromgit import cloneData
from DemoCovidProject.toRDS import sendToRDS
from DemoCovidProject.emrsc import runemr

with DAG(
    dag_id='Demo_covid_project',
    start_date= datetime(2022,11,2),
    schedule_interval='* * * 1 *',
    dagrun_timeout=timedelta(hours=2),
    catchup=False,
    default_args={
        'owner':'Meet',
        'depends_upon_past':False,
        'retries':0
    }
)as dag:
    Start_Pipeline = EmptyOperator(
        task_id = 'Start'
    )
    Stop_Pipeline = EmptyOperator(
        task_id = 'Stop'
    )

    clonedata= PythonOperator(
    task_id='Clone_data_from_git',
    python_callable=cloneData,
    dag=dag
    )

    sendtords= PythonOperator(
    task_id='Data_to_RDS',
    python_callable=sendToRDS,
    dag=dag
    )

    sendToEMR = PythonOperator(
        task_id = 'Running_Data_Clean_On_EMR',
        python_callable=runemr,
        dag=dag
    )
    
    Start_Pipeline>>clonedata>>sendtords>>sendToEMR>>Stop_Pipeline