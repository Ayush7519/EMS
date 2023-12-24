
echo "BUILD START"÷

# python3.10 -m pip install -r requirements.txt
pip install -r requirements.txt

# python3.10 manage.py collectstatic --noinput --clear --directory staticfiles_build
python manage.py collectstatic 
# echo "BUILD END"