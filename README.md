1. Create a virtual environment and activate it 
#change directory to EWallet
2. install python packages  in the requirments.txt file 
   using pip install -r requirments.txt
3. Apply migrations 
    using python python manage.py migrate
4. Start application 
    using python manage.py runserver (the project will run on port 8000 by default so you need to add port in api requests as well. Inorder to remove port we have to kill the normal http port(80) service)