Ran `ALTER ROLE tv_backend SET search_path TO tv_backend` to point tv_backend to the correct schema.

The below are useful for checking migrations
`python manage.py migrate --plan`
`python manage.py sqlmigrate model 0001` (model and 0001 from the above)

vscode and heroku can handle multiline env vars - using \n in terminal though breaks the ssl files