## MemeCaption API

A python+flask learning project.

#### Usage

* /templates - Displays meme templates from /static/ folder and their id

<strong> Generates a meme based on text input</strong>

* /homebrew?id={meme_id}&upper={upper_text}&lower={lower_text}&x={x_offset}&y={y_offset} 

* /dogfact - returns random dogfact

* /upload?pass={token} - Interface for uploading files
* / - Current status of api 

* Example of database in /templates/db.json

If you want to to use firebase add your own config:
<strong>serviceAccountKey.json</strong>

For SQLAlchemy: 
<strong>credentials.json</strong>
```
{"url":  "yourip",
  "user": "your_user",
  "password": "your_password",
  "database": "your_db",
  "token": "your_token"
}
```
#### Dependencies
Found in
<strong>req.txt</strong>

```
pip install -r req.txt
```
