echo "BUILD START"
python3.10 -m pip install requiremnets.txt
python3.10 manage.py collectstatic --noinput --clear
encho "BUILD END"