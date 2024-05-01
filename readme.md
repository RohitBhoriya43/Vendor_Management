
# Vendor Management System

Firstly create a python virual environment
```bash
  python -m venv venv
```
Activate the virual Environment 1 (windows)
```bash
  source venv/Scripts/activate
```
Activate the virual Environment 2 (mac/linux)
```bash
  . venv/bin/activate
```

Install the requirements.txt file
```bash
  pip install -r requirements.txt
```
Run the django project
```bash
  python manage.py runserver 3000
```

All vendor api like GET,POST,PUT,DELETE basic token or superuser token is valid







## New Basic Token Create APi


```http
  Post /api/vendor/basic_user_created/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. Your username |
| `password` | `string` | **Required**. Your password |

#### Super User create command
```bash
  python manage.py createsuperuser
```
## Super User Login

```http
  POST /api/vendor/superuser_login/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**.  |
| `password`      | `string` | **Required**.  |



All Purchase order api like GET,POST,PUT,DELETE vendor token is valid

## Vendor token generate api
```http
  GET /api/vendors/${vendor_id}/
```

#### Token assign for the headers 

```http
  {
    "Authorization":"Token ${vendor_token}"
  }
```



