Setup Bruno to generate bruno collection but they are already committed.
`npm install -g @usebruno/cli`

[Install Bruno](https://www.usebruno.com/) and open the collection from bruno collection if you want to mess with the endpoints. You'll need to [create an environmet](https://docs.usebruno.com/variables/environment-variables) and add `baseUrl` with a value of `http://localhost:8000`

[Setup Poetry if you want](https://python-poetry.org/docs/) but running `docker compose up --build` will install and work with poetry in the container.

Docker will spin up the app, and a postgres DB that it initializes with seed data from `data/init.sql`
