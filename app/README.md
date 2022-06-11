# disgenet-ms
A reusable micro service to provide Disgenet apis on a local machine (data is stored locally)

**Build the image**: docker-compose build
**Run the service**: docker-compose up

**All VDA's**: http://127.0.0.1:8000/api/vda/variants

**Example url for a single VDA**: http://127.0.0.1:8000/api/vda/variants/rs295

**Filter parameters**: 'year', 'source', 'score', 'ei', 'pmid'

**Example url with a filter**: http://127.0.0.1:8000/api/vda/variants?year=2000