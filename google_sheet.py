import pandas as pd
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account


def upload_df_to_sheet(
    *, spreadsheet_id: str, df: pd.DataFrame, range_name: str = "Sheet1!A1"
) -> None:

    credentials = service_account.Credentials.from_service_account_file(
        'application_default_credentials.json', 
        scopes=[
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/spreadsheets"
            ]
        )

    service = build("sheets", "v4", credentials=credentials)

    try:
        service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range=(tt := range_name.split("!"))[0] + f"!{tt[1]}:Z",
            body={},
        ).execute()
    except:
        sheet_name = range_name.split("!")[0]
        body = {"requests": {"addSheet": {"properties": {"title": f"{sheet_name}"}}}}
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body
        ).execute()
    finally:
        df.fillna("", inplace=True)
        # Convert the DataFrame to a list of lists
        data = [df.columns.values.tolist()] + df.values.tolist()
        # Prepare the request body for the API to update the sheet
        body = {"values": data}

        # Update the spreadsheet with the DataFrame's data
        _ = (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )


def upload_image_to_sheet(
    spreadsheet_id: str,
    image_path: str,
    sheet_name: str = "Sheet1",
    cell_range: str = "A1",
) -> None:
    """
    Uploads a local image to Google Sheets via Drive.

    Args:
        spreadsheet_id: ID from Sheets URL (e.g. "1abc...xyz")
        image_path: Path to local PNG/JPG file
        sheet_name: Target sheet name
        cell_range: Target cell (e.g. "B2")
    """
    # Authenticate once for both APIs
    scopes_ = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = service_account.Credentials.from_service_account_file(
        'application_default_credentials.json', 
        scopes=[
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/spreadsheets"
            ]
        )


    # --- Step 1: Upload image to Drive ---
    drive_service = build("drive", "v3", credentials=credentials)

    file_metadata = {
        "name": "Sheet Image Upload",
        "mimeType": "image/png" if image_path.lower().endswith(".png") else "image/jpeg",
    }

    media = MediaFileUpload(image_path, mimetype=file_metadata["mimeType"])
    uploaded = (
        drive_service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )

    # Make publicly viewable
    drive_service.permissions().create(
        fileId=uploaded["id"], body={"type": "anyone", "role": "reader"}
    ).execute()

    image_url = f"https://drive.google.com/uc?id={uploaded['id']}"

    # --- Step 2: Insert into Sheets ---
    sheets_service = build("sheets", "v4", credentials=credentials)

    # Use IMAGE() formula
    formula = f'=IMAGE("{image_url}")'

    sheets_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!{cell_range}",
        valueInputOption="USER_ENTERED",
        body={"values": [[formula]]},
    ).execute()

    print(f"Successfully inserted image at {sheet_name}!{cell_range}")
