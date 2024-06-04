# JobHunter
 Script for searching specific company job websites for new postings.



# Packages installed via terminal
Written using python 3.12.3

```
pip install beautifulsoup4
pip install lxml
# Loaded by default?
pip install requests
# If requests works, playwright is unnecessary
pip install pytest-playwright
playwright install
pip install simplegmail
pip install datatable
# Also installs numpy
pip install pandas
```

### Building and running your application

When you're ready, start your application by running:
`docker compose up --build`.

Your application will be available at http://localhost:8000.

### Deploying your application to the cloud

First, build your image, e.g.: `docker build -t myapp .`.
If your cloud uses a different CPU architecture than your development
machine (e.g., you are on a Mac M1 and your cloud provider is amd64),
you'll want to build the image for that platform, e.g.:
`docker build --platform=linux/amd64 -t myapp .`.

Then, push it to your registry, e.g. `docker push myregistry.com/myapp`.

Consult Docker's [getting started](https://docs.docker.com/go/get-started-sharing/)
docs for more detail on building and pushing.

### References
* [Docker's Python guide](https://docs.docker.com/language/python/)