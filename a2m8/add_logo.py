import os
import fitz
from PIL import Image
import tempfile
def doaddlogo(path, logo_path, terminal):
    logo = Image.open(logo_path)
    logo = logo.convert('RGBA')  # Add this line to convert logo to RGBA color mode

    # Set padding for logo
    padding = 10

    # Loop through all files in directory
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)

        # Check if file is a JPEG
        if os.path.isfile(filepath) and filename.lower().endswith('.jpg') or os.path.isfile(filepath) and filename.lower().endswith('.tiff') or os.path.isfile(filepath) and filename.lower().endswith('.tif') or os.path.isfile(filepath) and filename.lower().endswith('.png'):
            terminal.appendPlainText(f"Adding logo to {filename}...")

            # Open JPEG image
            img = Image.open(filepath)
            img = img.convert('RGB')

            # Resize logo to fit in bottom right corner
            logo_size = int(min(img.size[0], img.size[1]) * 0.16)
            logo_resized = logo.resize((logo_size, logo_size), resample=Image.LANCZOS).convert('RGBA')

            # Calculate position for logo
            x_offset = img.size[0] - logo_resized.size[0] - padding + 75
            y_offset = img.size[1] - logo_resized.size[1] - padding
            pos = (x_offset, y_offset)
            
            # Paste logo onto image
            img.paste(logo_resized, pos, mask=logo_resized)

            # Save image with logo
            new_filename = f"modified_{filename}"
            new_filepath = os.path.join(path, new_filename)
            img.save(new_filepath)

            # Close image file
            img.close()

            # Remove original file
            os.remove(filepath)
            terminal.appendPlainText(f"Deleted {filename}")
            os.rename(new_filepath,filepath)

        # Check if file is a PDF
        elif os.path.isfile(filepath) and filename.lower().endswith('.pdf'):
            terminal.appendPlainText(f"Adding logo to {filename}...")

            # Open PDF file
            pdf = fitz.open(filepath)

            # Get first page
            page = pdf[0]

            try:
                # Create image from page
                pix = page.get_pixmap()
                with tempfile.NamedTemporaryFile(suffix='.png') as f:
                    pix.writePNG(f.name)
                    img = Image.open(f.name)
                    img = img.convert('RGBA')
            except Exception as e:
                terminal.appendPlainText(f"Error: {e}")
                continue
            # Resize logo to fit in bottom right corner
            logo_size = int(min(img.size[0], img.size[1]) * 0.16)
            logo_resized = logo.convert('RGBA').resize((logo_size, logo_size))

            # Calculate position for logo
            x_offset = img.size[0] - logo_resized.size[0] - padding + 100
            y_offset = img.size[1] - logo_resized.size[1] - padding
            pos = (x_offset, y_offset)

            # Paste logo onto image
            img.paste(logo_resized, pos, logo_resized)

            # Create new PDF file with logo on the first page
            new_filename = f"modified_{filename}"
            new_filepath = os.path.join(path, new_filename)
            pdf_writer = fitz.Document()
            pdf_writer.insert_pdf(pdf, from_page=0, to_page=0)
            pdf_writer.save(new_filepath)

            # Add the rest of the pages to the new PDF file
            for i in range(1, len(pdf)):
                pdf_writer.insert_pdf(pdf, from_page=i, to_page=i)

            # Close PDF files
            pdf.close()
            pdf_writer.close()

            # Remove original file
            os.remove(filepath)
            terminal.appendPlainText(f"Deleted {filename}")
            os.rename(new_filepath,filepath)

    # Close logo image
    logo.close()
