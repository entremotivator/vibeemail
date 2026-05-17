# 🎉 Birthday Photo Frame App - Setup Guide

## Quick Start

This guide will help you set up the 80th Birthday Photo Frame application with Gmail and Google Drive integration.

---

## Step 1: Gmail Setup (for Email Functionality)

### Prerequisites
- A Gmail account
- 2-Factor Authentication enabled on your Gmail account

### Instructions

1. **Enable 2-Factor Authentication**
   - Go to [myaccount.google.com](https://myaccount.google.com)
   - Click "Security" in the left menu
   - Scroll to "2-Step Verification" and enable it if not already done

2. **Generate an App Password**
   - Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   - Select "Mail" and "Windows Computer" (or your device type)
   - Click "Generate"
   - Copy the 16-character password shown

3. **Update `.streamlit/secrets.toml`**
   ```toml
   [gmail]
   email = "your-email@gmail.com"
   password = "xxxx xxxx xxxx xxxx"  # Paste your 16-char app password here
   ```

---

## Step 2: Google Drive Setup (for Cloud Storage)

### Prerequisites
- A Google account with Google Drive access
- Access to Google Cloud Console

### Instructions

1. **Create a Google Cloud Project**
   - Go to [console.cloud.google.com](https://console.cloud.google.com)
   - Click the project dropdown at the top
   - Click "NEW PROJECT"
   - Enter a name (e.g., "Birthday Photo App")
   - Click "CREATE"

2. **Enable Google Drive API**
   - In the Cloud Console, go to "APIs & Services" → "Library"
   - Search for "Google Drive API"
   - Click on it and press "ENABLE"

3. **Create a Service Account**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "Service Account"
   - Fill in the details:
     - Service account name: `birthday-photo-app`
     - Click "CREATE AND CONTINUE"
   - On the next screen, click "CONTINUE" (you can skip optional steps)
   - Click "DONE"

4. **Generate a JSON Key**
   - Go back to "APIs & Services" → "Credentials"
   - Under "Service Accounts", click on the account you just created
   - Go to the "KEYS" tab
   - Click "Add Key" → "Create new key"
   - Choose "JSON" and click "CREATE"
   - A JSON file will download automatically

5. **Update `.streamlit/secrets.toml`**
   - Open the downloaded JSON file with a text editor
   - Copy the entire contents
   - Paste it into your `secrets.toml` file under `[google_drive]`:
   
   ```toml
   [google_drive]
   type = "service_account"
   project_id = "..."
   private_key_id = "..."
   private_key = "..."
   client_email = "..."
   client_id = "..."
   auth_uri = "..."
   token_uri = "..."
   auth_provider_x509_cert_url = "..."
   client_x509_cert_url = "..."
   ```

6. **Share Google Drive Folder** (Optional but Recommended)
   - Create a folder in your Google Drive called "Birthday_Photos_80th"
   - Right-click the folder and select "Share"
   - Share it with the service account email (found in the JSON file as `client_email`)
   - Give it "Editor" permissions

---

## Step 3: Install Dependencies

```bash
cd /home/ubuntu/birthday_photo_app
pip install -r requirements.txt
```

Or install manually:
```bash
pip install streamlit pillow opencv-python google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

---

## Step 4: Run the Application

```bash
cd /home/ubuntu/birthday_photo_app
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## Step 5: Test the Application

1. **Capture or Upload a Photo**
   - Use the webcam or upload an image

2. **Apply the Frame**
   - Click "Apply Birthday Frame"

3. **Send a Test Email**
   - Enter your own email address
   - Click "Send Framed Photo via Email"
   - Check your inbox (may take a minute)

4. **Verify Google Drive Upload**
   - Go to your Google Drive
   - Check the "Birthday_Photos_80th" folder
   - You should see your framed photo there

5. **Check the CSV Log**
   - Scroll down in the app to see the email log
   - You should see an entry with your email and the Google Drive link

---

## Troubleshooting

### Email Not Sending

**Error: "Failed to send email"**
- Verify your Gmail credentials in `secrets.toml`
- Make sure you're using the 16-character app password, not your regular password
- Check that 2FA is enabled on your Gmail account
- Try sending a test email from Gmail to verify your account works

**Error: "SMTP connection failed"**
- Check your internet connection
- Verify Gmail SMTP settings are correct (smtp.gmail.com:465)
- Check if your firewall is blocking SMTP

### Google Drive Upload Fails

**Error: "Failed to authenticate Google Drive"**
- Verify the JSON service account credentials are correctly pasted in `secrets.toml`
- Make sure all quotes and special characters are preserved
- Check that the Google Drive API is enabled in Cloud Console

**Error: "Failed to create/access Google Drive folder"**
- Verify you've shared the folder with the service account email
- Check that the service account has Editor permissions
- Try creating the folder manually first

### Frame Not Overlaying

**Error: "Frame image not found"**
- Ensure `frame.png` exists in the app directory
- Run: `ls -la /home/ubuntu/birthday_photo_app/frame.png`
- If missing, copy it: `cp /home/ubuntu/upload/elease_benford_80th_birthday_tiktok_frame.png /home/ubuntu/birthday_photo_app/frame.png`

### Streamlit Won't Start

**Error: "ModuleNotFoundError"**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Try: `pip install streamlit --upgrade`

---

## File Locations

- **App**: `/home/ubuntu/birthday_photo_app/app.py`
- **Frame Image**: `/home/ubuntu/birthday_photo_app/frame.png`
- **Email Log**: `/home/ubuntu/birthday_photo_app/email_log.csv`
- **Secrets**: `/home/ubuntu/birthday_photo_app/.streamlit/secrets.toml`
- **README**: `/home/ubuntu/birthday_photo_app/README.md`

---

## Security Best Practices

1. **Never commit secrets to version control**
   - Add `.streamlit/secrets.toml` to `.gitignore`
   - Keep your app password and service account JSON private

2. **Use App Passwords for Gmail**
   - Never use your main Gmail password in the app
   - App passwords are more secure and can be revoked easily

3. **Limit Service Account Permissions**
   - Only grant the service account access to the specific folder
   - Use Editor permissions only (not Owner)

4. **Rotate Credentials Regularly**
   - Generate new app passwords periodically
   - Regenerate service account keys if compromised

---

## Deployment to Streamlit Cloud

To deploy this app on Streamlit Cloud:

1. Push your code to GitHub (without `secrets.toml`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app" and connect your GitHub repo
4. In the app settings, go to "Secrets"
5. Paste your `secrets.toml` content
6. Deploy!

---

## Support & Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Drive API Guide](https://developers.google.com/drive/api/guides/about-sdk)
- [Gmail API Guide](https://developers.google.com/gmail/api/guides)
- [Google Cloud Console](https://console.cloud.google.com)

---

## Next Steps

Once everything is working:
1. Customize the email message in `app.py`
2. Add more frame designs
3. Deploy to Streamlit Cloud for public access
4. Share the link with your guests!

Enjoy your 80th Birthday Photo Frame App! 🎉
