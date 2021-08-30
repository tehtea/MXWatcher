# MXWatcher

This is a submission for a take-home assignment by Abnormal Security. The requirement is to create a service which runs a daily job and outputs some kind of storage format which can give insights to the email service used by a company if given its email domain.

The gist of this solution is that this service will run a daily cron job which does the following:
1. Perform DNS lookup for MX records on each valid domain in the list of companies
2. If a MXRecord does not exists yet, do an IPInfo query for the domain found in the first MX record of a company. This can be used to infer the email service used.
3. Also, if a MXRecord does not exist yet but there was a previous MXRecord for the company, do a soft delete on that stale MXRecord.

Environment:
- Google Cloud
- Google App Engine
- Python 3.7
- PostgreSQL 13 engine
- Ubuntu 18.04 for development machine, with SQLite used as local DB
- TypeScript and React on the frontend

The entire code base is designed with running on Google App Engine in mind, since it natively supports the scheduling of cron jobs.
Data Persistence is provided through the use of Cloud SQL (with a Postgres 13 engine),
and secure storage of secrets is done through Cloud Secret Manager.

## Other design considerations / noteworthy implementation details  

Backend:
1. To reduce IPInfo queries (since there is a monthly quota), IPInfo is not further requested if there is no change to the MXRecord for a company
2. Relational DB was used since there are no real-time requirements and the entities happened to be easily mapped in a relational manner
3. Object Schemas are in `datastore.py` but there are broadly three entities, `Company`, `MXRecord`, and `ResolvedMXRecordIP`
4. Secrets are stored within Cloud Secret Manager rather than the source code
5. Defensive programming and designing by contract throughout the codebase

Frontend:
1. `TypeScript` for easy code management event if SLOC increases
2. Use of `Redux` for scalability as a store slice can be created for each functionality
3. Utilization of `react-query` library to handle success and failure scenarios for xHR calls in a declarative manner, making the code cleaner

## Usage
- For a deployed demo, the base URL is https://abnormal-security-interview.wl.r.appspot.com/.
- To see an example of what a company with a recently changed record will look like, search for `DEBUG_INC` in demo web app.
- To initiate the crawling manually, go to `/crawlMXRecords`. You can do it on first run for local testing.

To run locally for testing, do the following:
1. In the `frontend/` folder, run `npm install`, followed by `npm run build`

Then, in the `backend/` folder:

2. Create an account at [IPInfo](https://ipinfo.io/)
3. Copy the token in your IPInfo account and replace the placeholder value for the `_ipInfoAccessToken` variable in `crawler.py` with the token 
4. Run `pip install -r requirements.txt`
5. Run `python main.py`, and go to `localhost:5000` to access the demo application. To seed data, initialize crawling by going to `localhost:5000/crawlMXRecords`


## Testing
Unit Testing is implemented on the crawler as that is the most critical functionality in this service.

Furthermore, there is one path in the code that will usually not be touched - i.e. what happens when the email provider for a company has changed.

1. Run `pip install -r requirements.txt` if you haven't
2. Copy the token in your IPInfo account and replace the placeholder value for the `_ipInfoAccessToken` variable in `crawler.py` with the token 
3. From the project root, cd to `/backend`
4. Run `python -m unittest test_crawler.py`