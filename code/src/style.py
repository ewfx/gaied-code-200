css="""
/* ✅ Ensure Entire Page is White with Black Text */
body, .gradio-container { 
    background-color: white !important; 
    color: black !important;
}

/* ✅ Make Headings Black */
h2, h3, h4 { 
    color: black !important; 
}

/* ✅ Make "Upload Files" and "Results" Headers Red */
#file-upload label, #results-header {
    background-color: red !important; 
    color: white !important; 
    font-weight: bold !important;
    padding: 10px;
    border-radius: 5px;
    text-align: center;
}

/* ✅ Style the File Upload Box */
#file-upload { 
    background-color: white !important; 
    border: 1px solid black !important; 
    color: black !important; 
}

/* ✅ Make "Classify" Button Red */
#classify-btn { 
    background-color: #333333 !important; 
    color: white !important; 
    font-size: 18px; 
    border-radius: 8px; 
    padding: 10px 20px; 
}

/* 🔴 Ensure Outer Container is RED */
#output-container {
    background-color: red !important;
    padding: 20px !important;
    border-radius: 8px !important;
    border: 1px solid black !important;
}

/* ⚪ Ensure Inner Box is WHITE */
#output-box {
    background-color: #333333 !important;
    color: black !important;
    font-weight: bold !important;
    padding: 15px !important;
}

/* Ensure textarea inside the output box is also white */
#output-box textarea {
    background-color: white !important;
    color: black !important;
    font-weight: bold !important;
    border: none !important;
    width: 100% !important;
}

/* ✅ Make Results Text Bold Black */
#output-box p, .output-box p, #output-container p, .output-container p {
    color: black !important;
    font-weight: bold !important;
}

/* 📝 Ensure Result Text is BOLD */
#output-box, #output-box p, #output-box textarea {
    font-weight: bold !important;
}
"""