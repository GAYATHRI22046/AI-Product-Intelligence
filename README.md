# ⚙️ AI Product Intelligence

An AI-powered system that analyzes industrial product information from **PDFs, websites, and manual inputs** to extract specifications, identify information gaps, detect conflicting data, and generate supplier questions.

## 💡 How It Works

**Extract → Understand → Verify**

- 📄 Extract information from PDFs, websites, and manual inputs
- 🤖 Organize and understand product specifications using AI
- ⚠️ Detect missing information and conflicting values
- ❓ Generate supplier questions
- 📊 Calculate an intelligence score
- 🔗 Provide evidence traceability

## 🛠️ Tech Stack

Python • Streamlit • Google Gemini API • PyMuPDF • BeautifulSoup • Requests

## 🧪 How to Test

AI Product Intelligence accepts three real-world product information sources:

1. Manual Information
2. Product PDF
3. Product Website URL

### Example Product

**Mitsubishi Electric SF-PRO 2.2 kW 4P IP55 Three-Phase Motor**

**Manual Information:**
Paste the following:

Product: Mitsubishi Electric SF-PRO 2.2 kW 4P IP55

Phase: 3
Model: SF-PRO
Rated output: 2.2 kW
Poles: 4
Rated voltage: 380 / 400 / 415 V
Rated frequency: 50 Hz
Rated current: 5.3 A
Rated speed: 1500 RPM
Efficiency class: IE3
Thermal class: 120(E)
Rating: S1 continuous
Enclosure: Totally enclosed fan cooled
Protection: IP55
Cooling method: IC411
Frame: 100L
Weight: 29 kg
Installation: Foot mounted

**Product PDF:**

[Official Mitsubishi Electric Specification PDF](https://www.mitsubishielectric.com/fa/id_en/products/drv/induction/download/2-Three-Phase-Motor-IE3/2-Foot-Mounted-Outdoor-IP55/2-400V-class/spec-sf-pro-2-2k-w-4p-ip55-400v.pdf)

If the PDF does not open when clicked, copy the link and open it directly in a new browser tab.

**Product Website:**

[Official Mitsubishi Electric Product Page](https://www.mitsubishielectric.com/fa/id_en/products/drv/induction/items/tpmie3/foot-mounted-outdoor.html)

If the website does not open when clicked, copy the link and open it directly in a new browser tab.

Click **Analyze Product** to extract specifications, identify information gaps, detect conflicting information, generate supplier questions, calculate the intelligence score, and provide evidence traceability.
