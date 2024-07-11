import streamlit as st
from pathlib import Path
import google.generativeai as genai
from api_key import api_key

# configure genai with api key
genai.configure(api_key=api_key)

#setting up the model
generation_config = {
  "temperature": 0.4,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 4096,
}

#apply safety settings
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

# prompt used to genearte response using genai
system_prompt=""" 
As a highly skilled medical practitioner specializing in image analysis,you are tasked with examining medical images for a renowned hospital.Your expertize is crucial in identifying any anomalies,diseases,or health issues that may be present in the image

Your Responsibilities:

1.Detailed Analysis:Thouroughly analayze each image,focusing on identifying any abnormal findings.
2.Findings Report:Document all observed anomalies or signs of diseases.Clearly articulate these findings in a structured format.
3.Recommendation and Next Steps:Based on your analysis,suggest potential next steps,including further test and treatment as applicable.
4.Treatment Suggestions: If appropriate,recommend possible treatment options or interventions.

Important Notes:
1.Scope of Response:only respond if the image pertains to human health issues.
2.Clarity of Image:In cases where the imagee quality impedes clear analysis, note that certain aspects are 'Unable to be determined based on provided image.'
3.Disclaimer:Accompany your analysis with the disclaimer:"Consult with a doctor before making any decisions."
4.Your insights are invaluable in guiding clinical decisions.Please proceed with the analysis,adhering to the structured approach outlined above.


Please provide me an output response with these 5 headings:.Detailed Analysis,Findings Report,Recommendation and Next Steps,Treatment Suggestions,Disclaimer
"""

#model configuration
model = genai.GenerativeModel(model_name="gemini-1.0-pro-vision-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)



#setting page config
st.set_page_config(page_title="Medi Buddy", page_icon=":robot: ")

#set the title
st.title("👩🏻‍⚕️❤️Medi Buddy 📊👨🏻‍⚕️")

#set the subheader
st.subheader("An application that  help users to identify medical diseases based on images")

#sidebar
with st.sidebar:
   st.title("Upload Image")
   #upload files
   uploaded_file=st.file_uploader("Upload the medical image for analysis",type=["jpg","png","jpeg"])
   

   submit_button=st.button("Analyze")

#showing the uploaded image on screen
if uploaded_file:
       st.image(uploaded_file,width=500,caption="Uploaded Medical Image")
       
if submit_button:
      #process the uploaded image
      image_data=uploaded_file.getvalue()

      # making our image ready
      image_parts = [
        {
          "mime_type": "image/jpeg",
          "data": image_data
        },
      ]
      # making our prompt ready
      prompt_parts = [
         image_parts[0],
         system_prompt,
       ]
      
     # Genearte a response based on prompt and image
      
      response = model.generate_content(prompt_parts)

      if response:
         st.title("Here is the analysis based on your image: ")
         st.write(response.text)

