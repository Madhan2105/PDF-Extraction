import PyPDF2
import re
import os
import constants as CONSTANTS


def extract_text():
    # pdfFileObj = open('Receipt_09Nov2021_222247.pdf', 'rb')
    current_pdf_dir = os.path.join(os.getcwd(), CONSTANTS.PDF_DIR)
    for filename in os.listdir(CONSTANTS.PDF_DIR):
        file = os.path.join(current_pdf_dir, filename)
        if os.path.isfile(file):
            pdfFileObj = open(file, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            pageObj = pdfReader.getPage(0)
            text = pageObj.extractText()
            text = text.strip()
            output = {}
            output['Total'] = re.findall(r'Total\s₹\s*(\d+\.\d+)', text)[0]
            output["Name"] = re.findall(r'You rode with (\w+ ?\w+)', text)[0]
            output['License Plate'] = re.findall(r'License Plate: (\w+)',
                                                 text)[0]
            output['Source'] = re.findall("\\|(\s*[a-zA-Z\s,\d]*)(?:\\n|$)",text)[0].replace("\n", " ") # noqa
            output['Destination'] = re.findall(r'\\|(\s*[a-zA-Z\s,\d]*)\s(UberAuto|Uber Auto)', text)[0][0].replace("\n", " ") # noqa
            pdfFileObj.close()
    return output


if __name__ == "__main__":
    extract_text()
