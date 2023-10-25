echo "Build Started"
python3 -m pip install -r requirements.txt
python3 -m pip install psycopg2-binary

python3 manage.py collectstatic --noinput --clear
echo "Build Ended"