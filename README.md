
# citequery

Query citations of a set of [Pubmed](https://pubmed.ncbi.nlm.nih.gov/) articles. 

| browser view | feed view ([Thunderbird](https://www.thunderbird.net)) |
|:---:|:---:|
| ![screenshot_html](https://user-images.githubusercontent.com/20538437/154291838-b1d69eb4-b21e-4864-ac66-3d94072e9e94.png) | ![screenshot_rss](https://user-images.githubusercontent.com/20538437/154291848-079c7a60-92ce-45b8-b514-55215c1254b5.png) |

## Requirements and installation
 * [tornado](https://www.tornadoweb.org/) webserver
 * [lxml](https://lxml.de/) for parsing responses from the 
[entrez API](https://www.ncbi.nlm.nih.gov/home/develop/api/)

```
pip3 install lxml tornado
```

## Parameters in `src/config.py`
 * `apikey`: [API key](https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/) 
that can be appended as `get` parameter to API queries
 * `port`: where the webserver will listen
 * `serveraddress`: where this tool can be reached
 * `eutils_base`: remote location where E-utilities can be queried
 * `staticpath`: path to static files (`./static`)
 * `apptitle`: title that is displayed in the interface
 * `retmax`: maximum number of articles obtained in a search query
 * `showentrieshtml`: maximum number of articles displayed in a HTML response
 * `showentriesrss`: maximum number of articles displayed in a RSS response
 * `chunksize`: maximum number of articles that are loaded per API query
 * `cachefile`: local `.json`-filename for persisting fetched Pubmed records
 * `logfile`: local filename where logging information is written during operation
 * `examples`: dictionary of captions and sample queries

## Starting and stopping server

```
nohup python3 server.py > nohup.out 2>&1 & echo $! > pid.txt

kill -s SIGTERM $(<pid.txt)
```

