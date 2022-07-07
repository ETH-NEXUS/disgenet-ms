# Disgenet Micro Service

A reusable micro service to provide Disgenet apis and data on a local machine.

## Usage

To use the microservice in your application you need to integrate the following configuration into your `docker-compose.yml`

```yaml
version: "3"

services:
  disgenet:
      image: ethnexus/disgenet-ms
      volumes:
        - ./data:/data:z
      ports:
        - "9077:9077"
      secrets:
        - disgenet_creds
      env_file: .env
  secrets:
    disgenet_creds:
      file: ./.disgenet_creds
```

In your `.env` file adjust the required environment variables (if the values are not set the defaults as below are taken):

```bash
DISGENET_DB_URL=https://www.disgenet.org/static/disgenet_ap1/files/sqlite_downloads/current/disgenet_2020.db.gz
DISGENET_UMLS_URL=https://www.disgenet.org/static/disgenet_ap1/files/downloads/disease_mappings_to_attributes.tsv.gz
```

Create the disgenet credentials file:

```bash
echo "${DISGENET_USERNAME}:${DISGENET_PASSWORD}" | base64 > .disgenet_creds
```

Run the container using:

```bash
docker-compose up -d
```

## Using the API

### All VDA's
```
/api/vda/variants
```


### Example url for a single VDA 
```
/api/vda/variants/rs295
```

### Filter parameters

- **year**: some description (e.g. Examplevalue)
- **source**: some description (e.g. Examplevalue)
- **score**: some description (e.g. Examplevalue)
- **ei**: some description (e.g. Examplevalue)
- **pmid**: some description (e.g. Examplevalue)

You can provide multiple of those parameters as query parameters in the url:
```
/api/vda/variant?year=2000&source=UNIPROT
```

