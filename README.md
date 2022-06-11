# disgenet-ms
A reusable micro service to provide Disgenet apis on a local machine (data is stored locally)

## Database
To reproduce the code locally, you need to download the sqlite database and paste it inside the outer /app directory (on the same level with the manage.py file)

Link to the DB:
https://drive.google.com/drive/folders/1if1GJLRlihQX44QjLT1uMMVfG7ZyIefd?usp=sharing

NB! Don't use the DB downloaded from https://www.disgenet.org/api/  because it had to be change for this app. 

**Build the image**: docker-compose build

**Run the service**: docker-compose up

**All VDA's**: http://127.0.0.1:8000/api/vda/variants

**Example url for a single VDA**: http://127.0.0.1:8000/api/vda/variants/rs295

**Filter parameters**: 'year', 'source', 'score', 'ei', 'pmid'

**Example url with a filter**: http://127.0.0.1:8000/api/vda/variants?year=2000

