# gcloud_plico
## GCE SSH LOGIN PROCEDURE:
    1 - gcloud auth login
    2 - gcloud compute ssh gcloud-plico-vm
source venv/bin/activate
python -m gunicorn gcloud_plico.wsgi:application --bind 0.0.0.0:8000 --log-level debug
