
echo "BUILD START"

# Install project dependencies
python3.10 -m pip install -r requirements.txt

# Collect static files to the correct output directory
python3.10 manage.py collectstatic --noinput --clear --directory staticfiles_build

echo "BUILD END"