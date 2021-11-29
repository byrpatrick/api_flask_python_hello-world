build:
	@docker build --rm -t auth0/api/flask-python/rbac-authorization .

run: build
	@docker run --rm -it -p "6060:6060" auth0/api/flask-python/rbac-authorization