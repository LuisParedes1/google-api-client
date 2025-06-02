# google-api-client

[Google Client APIs](https://github.com/googleapis/google-api-python-client) placeholders to use in projects

# Set Up

* To use Google Cloud services we need to have API access credentails for our project.
  * Go to [Google Cloud Console](https://console.cloud.google.com/)
  * Select a resource -> Create new project
  * Go to APIs & Services
  * Credentials -> Create Credentials -> API Keys

 * Copy the API Key and keep it safe.
  

# Google Sheets

* We need to manually create a spreadsheet within [Google Sheet](https://docs.google.com/spreadsheets/u/0/) and copy the spreadsheets ID

![spreadsheetsID](https://github.com/user-attachments/assets/0e9446c4-c03e-45c3-bf4b-5ec0d0b317b4)

* `upload_df_to_sheet` function uploads the Pandas Dataframe into `spreadsheet_id`.
* `upload_image_to_sheet` function uploads an image from `image_path` path into `spreadsheet_id`.
*  Using `range_name` parameter we can specify in which tab to insert our data and which cell to take as starting point.
