# HomeManager

## Run it locally

- Create `.env` file based on provided example file
  - `cp .env.example .env`
- Make sure variables used by docker-compose services are all set correctly in `.env` file
  - POSTGRES_HOST should be `postgres`
- In root folder run commands
  - `docker-compose build`
  - `docker-compose up -d`
- (optional) For debugging and easier management of docker services - [integrate remote interpreter with your IDE](https://www.jetbrains.com/help/pycharm/using-docker-compose-as-a-remote-interpreter.html)
- Application will be available on `localhost:8000`
- To run management commands (like `createsuperuser` or `collectstatic`) run:
  - `docker-compose exec django python ./manage.py <command>`
  
