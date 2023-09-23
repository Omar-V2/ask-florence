PROMPT_TEMPLATE = """
Your role is a medical doctor who is using a patient's Electronic Health
Records to give updates next of kin.

Under no circumstances should you ever give medical advice.

Under no circumstances should you ever give updates on conditions or
diagnoses which fall into the following categories:
{condition_deny_categories}

Answer the question based only on the following context taken
from a patient's Electronic Health Record. Under no circumstances should
you answer any questions that are not answerable using this context:
{context}

If you are unable to answer a query based on any of the above constraints,
you MUST reply with:
{user_deny_message}

Use the following dictionary of medical terms and their meanings if necessary:
{medical_dictionary}

Answer the following query:
{question}
"""

CONDITION_DENY_CATEGORIES = "\n".join([
    "Death",
    "Permanent and Terminal Illness",
    "Change of Quality of Life"
])

USER_DENY_MESSAGE = f"""
I'm sorry, as an AI system I cannot answer your query.

I cannot give you medical advice, or update you with any information on:
{CONDITION_DENY_CATEGORIES}

Please direct your query to a healthcare professional.
"""

MEDICAL_DICTIONARY = {
    "Admission (A&E)": "Entry into the Emergency Room",
    "AMU": "Acute Medical Unit, a specialized area for urgent care",
    "Ward Round Notes": "Regular check-up notes by doctors",
    "Pre-Discharge Assessment": "Final evaluation before sending patient home",
    "Follow-up": "Next scheduled doctor's appointment",
    "Plan": "Next steps in treatment or care",
    "C/O": "Complaining of",
    "CP": "Chest Pain",
    "Clin. Ex": "Clinical Examination",
    "JVP": "Jugular Venous Pressure, related to heart function",
    "ECG": "Electrocardiogram, a heart test",
    "ST depression": "A finding on the ECG that may indicate heart issues",
    "Rx": "Prescription or treatment",
    "GTN (Glyceryl Trinitrate) spray": "A spray for chest pain",
    "IV fluids": "Fluids given through a vein",
    "Clopidogrel": "A blood thinner medication",
    "Troponin": "A marker in the blood that can indicate heart damage",
    "FBC": "Full Blood Count, a general blood test",
    "NAD": "No Apparent Distress or No Abnormality Detected",
    "ACS": "Acute Coronary Syndrome, a range of conditions related to sudden, reduced blood flow to the heart",
    "PE": "Pulmonary Embolism, a lung-related condition",
    "NSTEMI": "Non-ST-elevation myocardial infarction, a type of heart attack",
    "Angina": "Chest pain due to reduced blood flow to the heart",
    "SOB": "Shortness of Breath",
    "Obs": "Observations, usually referring to vital signs like blood pressure and heart rate",
    "BP": "Blood Pressure",
    "Mobilising": "Moving around",
    "CVS": "Cardiovascular System, related to the heart and blood vessels",
    "MFFD": "Medically Fit For Discharge",
    "Heparin infusion": "Drip of a blood thinner medication",
    "Cardiology consult initiated": "Started consultation with heart specialists",
    "Refer to cardiology": "Send the patient's case to a heart specialist",
    "Probable Diagnosis": "Most likely medical condition based on current information",
    "Differential Diagnoses": "List of possible medical conditions that could explain the symptoms",
    "Preparing for discharge": "Getting ready to leave the hospital",
    "Drug reconciliation": "Making sure all medications are correctly listed before leaving the hospital"
}
