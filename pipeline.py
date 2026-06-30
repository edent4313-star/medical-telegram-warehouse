from dagster import op, job, In, Nothing, Definitions, ScheduleDefinition
import subprocess
import sys
import logging


@op
def scrape_telegram_data():
    subprocess.run(
        [sys.executable, "src/scraper.py"],
        check=True
    )


@op(ins={"start": In(Nothing)})
def load_raw_to_postgres():
    subprocess.run(
        [sys.executable, "src/load_raw_to_postgres.py"],
        check=True
    )


@op(ins={"start": In(Nothing)})
def run_dbt_transformations():
    subprocess.run(
        ["dbt", "run"],
        cwd="medical_warehouse",
        check=True
    )


@op(ins={"start": In(Nothing)})
def run_yolo_enrichment():
    subprocess.run(
        [sys.executable, "src/yolo_detect.py"],
        check=True
    )


@job
def medical_pipeline():

    scrape = scrape_telegram_data()
    load = load_raw_to_postgres(scrape)
    dbt = run_dbt_transformations(load)
    run_yolo_enrichment(dbt)


daily_schedule = ScheduleDefinition(
    job=medical_pipeline,
    cron_schedule="0 0 * * *"
)


defs = Definitions(
    jobs=[medical_pipeline],
    schedules=[daily_schedule]
)