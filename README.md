# google-api-client

[Google Client APIs](https://github.com/googleapis/google-api-python-client) placeholders to use in projects.

# Set Up

* To use Google Cloud services we need to have API access credentails for our project.

* See Creating authorization credentials for how to obtain a `client_secrets.json` file.

These credentials are needed to interact with different services.

```python
from google_auth_oauthlib.flow import InstalledAppFlow
...
flow = InstalledAppFlow.from_client_secrets_file(
    'path_to_directory/client_secret.json',
    scopes=['service_1', 'service_2', ...])
```
  

* See [Getting Started](https://googleapis.github.io/google-api-python-client/docs/start.html) for more info.

# Google Sheets

* We need to manually create a spreadsheet within [Google Sheet](https://docs.google.com/spreadsheets/u/0/) and copy the spreadsheets ID

![spreadsheetsID](https://github.com/user-attachments/assets/0e9446c4-c03e-45c3-bf4b-5ec0d0b317b4)

* `upload_df_to_sheet` function uploads the Pandas Dataframe into `spreadsheet_id`.
* `upload_image_to_sheet` function uploads an image from `image_path` path into `spreadsheet_id`.
*  Using `range_name` parameter we can specify in which tab to insert our data and which cell to take as starting point.
