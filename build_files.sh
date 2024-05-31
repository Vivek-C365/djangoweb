echo "BUILD START"
python3.9 -m pip install requiremnets.txt
python3.9 manage.py collectstatic --noinput --clear
encho "BUILD END"