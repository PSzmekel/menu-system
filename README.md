# menu-system
HOW TO RUN PROJECT
1) run postgres on docker e.g. 'docker run --name postgres -p5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres'
2) create .env file from env.sample
3) run 'pip install -r requirements.txt'
4) run python shell
5) run command 'from models inport db'
6) run command 'db.create_all()'
7) exit python shell
8) run command 'python api.py'
