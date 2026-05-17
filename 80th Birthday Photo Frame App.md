# 80th Birthday Photo Frame App

A Streamlit application that captures photos, overlays them with an elegant birthday frame, and automatically emails the result to guests while logging everything to Google Drive and a CSV file.

## Features

- 📸 **Photo Capture**: Use webcam or upload photos
- 🎨 **Frame Overlay**: Automatically applies the 80th birthday frame to photos
- 📧 **Auto Email**: Sends framed photos via Gmail
- ☁️ **Google Drive Storage**: Automatically uploads images to Google Drive
- 📊 **CSV Logging**: Tracks all emails sent and image links
- 💾 **Download**: Save photos locally

## Setup Instructions

### 1. Gmail Configuration

To enable email functionality, you need to:

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Find "App passwords" (only visible if 2FA is enabled)
   - Select "Mail" and "Windows Computer" (or your device)
   - Copy the generated 16-character password

3. **Add to `.streamlit/secrets.toml`**:
   ```toml
   [gmail]
   email = "your-email@gmail.com"
   password = "your-16-character-app-password"
   ```

### 2. Google Drive Configuration

To enable Google Drive storage:

1. **Create a Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the Google Drive API

2. **Create a Service Account**:
   - Go to "Service Accounts" in the Cloud Console
   - Create a new service account
   - Generate a JSON key
   - Download the JSON file

3. **Add to `.streamlit/secrets.toml`**:
   - Copy the entire JSON content from the downloaded file
   - Paste it under the `[google_drive]` section

4. **Share Google Drive Folder** (optional):
   - Create a "Birthday_Photos_80th" folder in your Google Drive
   - Share it with the service account email (found in the JSON file)

### 3. Install Dependencies

```bash
pip install streamlit pillow opencv-python google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv
```

### 4. Run the App

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## How to Use

1. **Capture or Upload Photo**:
   - Use the webcam to capture a live photo, or
   - Upload an existing image from your computer

2. **Apply Frame**:
   - Click "Apply Birthday Frame" to overlay the frame

3. **Send Photo**:
   - Enter the recipient's email address
   - Click "Send Framed Photo via Email"
   - The photo will be:
     - Uploaded to Google Drive
     - Emailed to the recipient
     - Logged to the CSV file

4. **Download**:
   - Use the "Download Framed Photo" button to save locally

5. **View Logs**:
   - Scroll down to see all emails sent and their Google Drive links

## File Structure

```
birthday_photo_app/
├── app.py                          # Main Streamlit application
├── .streamlit/
│   └── secrets.toml               # Configuration (Gmail & Google Drive)
├── email_log.csv                  # Auto-generated email log
└── README.md                      # This file
```

## CSV Log Format

The `email_log.csv` file contains:
- **Timestamp**: When the photo was sent
- **Email**: Recipient email address
- **Image Filename**: Filename of the processed image
- **Google Drive Link**: Direct link to the image on Google Drive

## Troubleshooting

### Email not sending
- Verify Gmail credentials in `secrets.toml`
- Ensure 2FA is enabled and app password is correct
- Check that Gmail allows "Less secure app access" (if not using app password)

### Google Drive upload fails
- Verify service account JSON is correctly formatted in `secrets.toml`
- Ensure the service account has access to the Google Drive folder
- Check that Google Drive API is enabled in Cloud Console

### Frame not overlaying correctly
- Ensure the frame image path is correct
- Verify the frame image exists at `/home/ubuntu/upload/elease_benford_80th_birthday_tiktok_frame.png`

## Security Notes

- **Never commit `secrets.toml` to version control**
- Keep your Gmail app password and Google Drive service account JSON private
- Use environment variables for production deployments

## Deployment

For production deployment on Streamlit Cloud:

1. Push code to GitHub (without `secrets.toml`)
2. Deploy on [Streamlit Cloud](https://streamlit.io/cloud)
3. Add secrets in the Streamlit Cloud dashboard:
   - Settings → Secrets
   - Paste your `secrets.toml` content

## Support

For issues or questions, refer to:
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Drive API Documentation](https://developers.google.com/drive/api/guides/about-sdk)
- [Gmail API Documentation](https://developers.google.com/gmail/api/guides)
