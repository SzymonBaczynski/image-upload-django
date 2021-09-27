# Image upload in DRF

## Quick start

### With existing database (from mail)
To run the project with existing database just simply run docker-compose:
```shell
$ docker-compose up
```

### Without existing database
In case you have the project from the github repository (without created db) you need migrate inside of the backend container:
```shell
$ docker-compose up
$ docker exec -it backend_container_hash_here bash # to get to the container
$ python manage.py makemigrations
$ python manage.py migrate
$ docker-compose restart
```
You need to create user on your own in that case.
## Admin Panel
```
http://localhost/admin/
```
Admin:
- username: admin
- password: admin

## API
Once you have the project up and running it is possible to test it.

### Authentication

**Important!** The service is intended to test in local environment due to it's preproduction settings.

```shell
$ curl -L -X POST 'http://localhost/api-token-auth/' -F 'username="admin"' -F 'password="admin"'

> {"token":"adc09a43ab9daa9d39260c3d089896066b2de559"}
```

Users existing in the db:
- username: admin password: admin with Enterprise plan (superuser)
- username: user01 password: user01 with Basic plan
- username: user02 password: user02 with Premium plan
- username: user03 password: user03 with Enterprise plan

### Check authentication

```shell
$ curl -L -X GET 'http://localhost/api/v1/' -H 'Authorization: Token adc09a43ab9daa9d39260c3d089896066b2de559'

> {
>    "username": "admin",
>    "userPlan": "Enterprise"
> }
```

### Upload image
```shell
$ curl -L -X POST 'http://localhost/api/v1/image-upload/' -H 'Authorization: Token adc09a43ab9daa9d39260c3d089896066b2de559' -F 'orginalImage=@"/C:/Users/user/Desktop/image.jpg"'

> {
>     "pk": 1
> }
```

### List user's images

```shell
$ curl -L -X GET 'http://localhost/api/v1/create-temp-link/' -H 'Authorization: Token adc09a43ab9daa9d39260c3d089896066b2de559'

> [
>    {
>         "pk": 1
>    }
> ]
```

### Create expiring (temporary) link

```shell
$ curl -L -X POST 'http://localhost/api/v1/create-temp-link/' -H 'Authorization: Token adc09a43ab9daa9d39260c3d089896066b2de559' -F 'image="1"' -F 'expiringTime="500"'
# image="<image_id>"
# expiringTime="<expiring-time>"

> "http://localhost/api/v1/temp-link/0bee55d1-95bc-454f-a25c-4777d6d102da/"
```

### Obtain original image

```shell
$ curl -L -X GET 'http://localhost/api/v1/original-image/1' -H 'Authorization: Token adc09a43ab9daa9d39260c3d089896066b2de559'
# http://localhost/api/v1/original-image/<image-id>

> [image]
```

### Obtain thumbnail image

```shell
$ curl -L -X GET 'http://localhost/api/v1/thumbnail-image/1/200' -H 'Authorization: Token aea6fee44f7baf797c86f724c8d11b761c220388' 
# http://localhost/api/v1/thumbnail-image/<image-id>/<thumbnail-size>

> [image]
```

## TODO
Possible bug's (not tested yet):
- behavior when provided image is smaller than thumbnail


