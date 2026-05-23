import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import csv
import os
from datetime import datetime
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import json

# Page configuration
st.set_page_config(page_title="Birthday Photo Frame Studio", layout="centered")

# Initialize session state
if 'processed_image' not in st.session_state:
    st.session_state.processed_image = None
if 'original_image' not in st.session_state:
    st.session_state.original_image = None
if 'selected_frame' not in st.session_state:
    st.session_state.selected_frame = "Elease Benford 80th Birthday"

# Frame configurations with cutout coordinates
FRAMES = {
    "Elease Benford 80th Birthday": {
        "file": "frame.png",
        "cutout_top": 14,
        "cutout_bottom": 1444,
        "cutout_left": 28,
        "cutout_right": 801,
        "title": "80th Birthday Celebration"
    },
    "Apostle Victor A. Howard Sr.": {
        "file": "apostle_victor_frame.png",
        "cutout_top": 375,
        "cutout_bottom": 1243,
        "cutout_left": 234,
        "cutout_right": 627,
        "title": "Birthday Dinner Celebration"
    }
}

# Title and description
st.title("🎉 Birthday Photo Frame Studio")
st.markdown("Capture your photo, choose a frame, and send it via email!")

# Frame selection
st.sidebar.header("🖼️ Frame Selection")
selected_frame_name = st.sidebar.radio("Choose a frame:", list(FRAMES.keys()))
st.session_state.selected_frame = selected_frame_name
frame_config = FRAMES[selected_frame_name]

# Load the selected frame image
frame_path = os.path.join(os.path.dirname(__file__), frame_config["file"])
if not os.path.exists(frame_path):
    st.error(f"Frame image not found at {frame_path}")
    st.stop()

frame_image = Image.open(frame_path)
st.sidebar.image(frame_image, caption=f"Selected: {selected_frame_name}", use_column_width=True)

# Helper function to overlay frame on photo with precise cropping
def overlay_frame_on_photo(photo_image, frame_image, frame_config):
    """Overlay the frame on the photo, cropping the photo to fit the exact cutout area."""
    cutout_top = frame_config["cutout_top"]
    cutout_bottom = frame_config["cutout_bottom"]
    cutout_left = frame_config["cutout_left"]
    cutout_right = frame_config["cutout_right"]
    
    cutout_width = cutout_right - cutout_left
    cutout_height = cutout_bottom - cutout_top
    
    # Get photo dimensions
    photo_width, photo_height = photo_image.size
    
    # Calculate aspect ratios
    cutout_aspect = cutout_width / cutout_height
    photo_aspect = photo_width / photo_height
    
    # Crop photo to match cutout aspect ratio
    if photo_aspect > cutout_aspect:
        # Photo is wider, crop width
        new_width = int(photo_height * cutout_aspect)
        left = (photo_width - new_width) // 2
        photo_cropped = photo_image.crop((left, 0, left + new_width, photo_height))
    else:
        # Photo is taller, crop height
        new_height = int(photo_width / cutout_aspect)
        top = (photo_height - new_height) // 2
        photo_cropped = photo_image.crop((0, top, photo_width, top + new_height))
    
    # Resize cropped photo to exact cutout dimensions
    photo_resized = photo_cropped.resize((cutout_width, cutout_height), Image.Resampling.LANCZOS)
    
    # Convert frame to RGBA if needed
    if frame_image.mode != 'RGBA':
        frame_rgba = frame_image.convert('RGBA')
    else:
        frame_rgba = frame_image
    
    # Convert resized photo to RGBA
    photo_rgba = photo_resized.convert('RGBA')
    
    # Create a new image with the frame size
    result = Image.new('RGBA', frame_image.size, (0, 0, 0, 0))
    
    # Paste the photo into the exact cutout position
    result.paste(photo_rgba, (cutout_left, cutout_top), photo_rgba)
    
    # Composite with frame on top
    result = Image.alpha_composite(result, frame_rgba)
    
    return result.convert('RGB')

# Helper function to get Google Drive service
def get_gdrive_service():
    """Authenticate and return Google Drive service."""
    try:
        creds_dict = st.secrets["google_drive"]
        creds = Credentials.from_service_account_info(creds_dict)
        service = build('drive', 'v3', credentials=creds)
        return service
    except Exception as e:
        st.error(f"Failed to authenticate Google Drive: {e}")
        return None

# Helper function to create or get Google Drive folder
def get_or_create_gdrive_folder(service, folder_name="Birthday_Photos"):
    """Get or create a Google Drive folder."""
    try:
        # Search for existing folder
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = service.files().list(q=query, spaces='drive', fields='files(id, name)', pageSize=10).execute()
        files = results.get('files', [])
        
        if files:
            return files[0]['id']
        
        # Create new folder if it doesn't exist
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        return folder.get('id')
    except Exception as e:
        st.error(f"Failed to manage Google Drive folder: {e}")
        return None

# Helper function to upload image to Google Drive
def upload_to_gdrive(service, image_path, folder_id):
    """Upload image to Google Drive folder."""
    try:
        file_metadata = {
            'name': os.path.basename(image_path),
            'parents': [folder_id]
        }
        media = MediaFileUpload(image_path, mimetype='image/jpeg')
        file = service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
        return file.get('webViewLink')
    except Exception as e:
        st.error(f"Failed to upload to Google Drive: {e}")
        return None

# Helper function to send email
def send_email_with_image(recipient_email, image_path, image_link, frame_name):
    """Send email with the framed photo."""
    try:
        gmail_user = st.secrets["gmail"]["email"]
        gmail_password = st.secrets["gmail"]["password"]
        
        # Create email
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = recipient_email
        msg['Subject'] = f"🎉 Your {frame_name} Photo Frame"
        
        # Email body
        body = f"""
        <html>
            <body>
                <h2>Happy Birthday! 🎉</h2>
                <p>Thank you for celebrating with us! Here's your framed birthday photo.</p>
                <p><strong>View your photo online:</strong> <a href="{image_link}">Click here</a></p>
                <p>Warm wishes,<br>The Birthday Team</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))
        
        # Attach image
        with open(image_path, 'rb') as attachment:
            image_data = attachment.read()
            image_part = MIMEImage(image_data)
            image_part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(image_path))
            msg.attach(image_part)
        
        # Send email
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

# Helper function to log to CSV
def log_to_csv(email, image_link, image_filename, frame_name):
    """Log email and image link to CSV."""
    csv_path = "/home/ubuntu/birthday_photo_app/email_log.csv"
    
    # Create CSV if it doesn't exist
    if not os.path.exists(csv_path):
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'Frame', 'Email', 'Image Filename', 'Google Drive Link'])
    
    # Append new entry
    with open(csv_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), frame_name, email, image_filename, image_link])

# Sidebar for configuration
st.sidebar.header("📋 Configuration")
use_camera = st.sidebar.checkbox("Use Webcam", value=True)
use_upload = st.sidebar.checkbox("Upload Photo", value=False)

# Photo capture section
st.header("📸 Capture or Upload Photo")

if use_camera:
    picture = st.camera_input("Take a picture")
    if picture is not None:
        st.session_state.original_image = Image.open(picture)

if use_upload:
    uploaded_file = st.file_uploader("Choose an image", type=['jpg', 'jpeg', 'png'])
    if uploaded_file is not None:
        st.session_state.original_image = Image.open(uploaded_file)

# Preview and process
if st.session_state.original_image is not None:
    st.subheader("Original Photo")
    st.image(st.session_state.original_image, use_column_width=True)
    
    # Process image with frame overlay
    if st.button("✨ Apply Birthday Frame", use_container_width=True):
        with st.spinner("Processing your photo..."):
            st.session_state.processed_image = overlay_frame_on_photo(
                st.session_state.original_image, 
                frame_image,
                frame_config
            )
        st.success("Frame applied successfully!")

# Display processed image
if st.session_state.processed_image is not None:
    st.subheader("Your Framed Photo")
    st.image(st.session_state.processed_image, use_column_width=True)
    
    # Save and email section
    st.header("📧 Send Your Photo")
    
    recipient_email = st.text_input("Enter recipient email address", placeholder="example@email.com")
    
    if st.button("🎁 Send Framed Photo via Email", use_container_width=True):
        if not recipient_email or '@' not in recipient_email:
            st.error("Please enter a valid email address")
        else:
            with st.spinner("Processing and sending..."):
                try:
                    # Save processed image temporarily
                    temp_image_path = f"/tmp/birthday_photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    st.session_state.processed_image.save(temp_image_path, quality=95)
                    
                    # Upload to Google Drive
                    gdrive_service = get_gdrive_service()
                    if gdrive_service:
                        folder_id = get_or_create_gdrive_folder(gdrive_service, "Birthday_Photos_Studio")
                        if folder_id:
                            image_link = upload_to_gdrive(gdrive_service, temp_image_path, folder_id)
                            
                            if image_link:
                                # Send email
                                if send_email_with_image(recipient_email, temp_image_path, image_link, selected_frame_name):
                                    # Log to CSV
                                    log_to_csv(recipient_email, image_link, os.path.basename(temp_image_path), selected_frame_name)
                                    
                                    st.success(f"✅ Photo sent successfully to {recipient_email}!")
                                    st.info(f"📁 View on Google Drive: [Click here]({image_link})")
                                else:
                                    st.error("Failed to send email")
                            else:
                                st.error("Failed to upload to Google Drive")
                        else:
                            st.error("Failed to create/access Google Drive folder")
                    else:
                        st.error("Google Drive authentication failed")
                    
                    # Clean up temp file
                    if os.path.exists(temp_image_path):
                        os.remove(temp_image_path)
                        
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    
    # Download option
    st.divider()
    st.subheader("💾 Download Photo")
    
    img_byte_arr = io.BytesIO()
    st.session_state.processed_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    st.download_button(
        label="Download Framed Photo",
        data=img_byte_arr,
        file_name=f"birthday_photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
        mime="image/png",
        use_container_width=True
    )

# View logs section
st.divider()
st.header("📊 Email Log")

csv_path = "/home/ubuntu/birthday_photo_app/email_log.csv"
if os.path.exists(csv_path):
    df = st.read_csv(csv_path)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No emails sent yet. Send your first photo to see the log!")
