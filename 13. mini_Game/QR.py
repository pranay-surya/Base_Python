# Install first (if not already installed):
# pip install qrcode[pil]

import qrcode

# Data to encode
data = "https://play.google.com/store/apps/details?id=com.gamma.scan"

# Create QR Code instance
qr = qrcode.QRCode(
    version=1,  # controls the size of the QR Code (1-40), higher = bigger
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # error correction level
    box_size=10,  # size of each "box" in pixels
    border=4,  # border thickness
)
# Add data
qr.add_data(data)
qr.make(fit=True)
# Generate image
img = qr.make_image(fill_color="black", back_color="white")
# Save image
img.save("qrcode.png")
print("QR Code generated and saved as qrcode.png")
