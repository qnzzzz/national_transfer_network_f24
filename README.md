# National Transfer Network

## Introduction
The National Transfer Network, or NTN, is an innovative initiative designed to address the college affordability crisis by facilitating smoother transitions for community college students to four-year universities. By streamlining the transfer process and enhancing success rates, NTN aims to reduce the total costs of obtaining a bachelor's degree and increase educational equity. The project leverages a digital platform to provide clear pathways for credit transfer, ensuring that students can achieve their academic goals without unnecessary delays or financial burdens. Through strategic partnerships with educational institutions and data-driven support systems, NTN seeks to make higher education more accessible and affordable, particularly for underserved and minority populations.

## Installaiton
1. Install Python 3
   ```bash
   pip install python3
2. Setup a virtual environment
   ```bash
   python3 -m venv venv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
3. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # MAC zsh
   venv\Scripts\activate.bat  # Windows cmd.exe
   source venv/bin/activate.csh  # Linux csh
4. Install required dependencies: 
   ```bash
   pip install -r requirements.txt
5. Install weasyprint
   ```bash
   python -m pip install weasyprint
6. Migrate the database and run server
   ```bash
   python3 manage.py makemigrations 
   python3 manage.py migrate
   python3 manage.py runserver
7. Load existing data into database
   ```bash
   python3 process_data.py # under ~/national_transfer_network_f24/ntn_app
   python3 manage.py load_data # under ~/national_transfer_network_f24
8. For issues with weasyprint:
   https://doc.courtbouillon.org/weasyprint/stable/first_steps.html
9. For issues with gobject: 
   https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
   

## Config
For accessing database, a config.ini file with MySQL username and password is required.

## Developers
Developers: Shuxin Liu, Yutian Qiu, Ella Liang, Howard Li, Shruti Ujlan 

All developers are from the Master of Information Systems Management program at Carnegie Mellon University's Heinz College. This project is developed as the 2024 Fall capstone project.

