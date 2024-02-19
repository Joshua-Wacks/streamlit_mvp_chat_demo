import streamlit as st
import urllib.request
import json
import os
import ssl

import numpy as np
from PIL import Image
from io import BytesIO
# import cv2

from azure.storage.blob import ContainerClient

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context
        
def getUserIcon(role):
    if(role == "assistant"):
        return """<?xml version="1.0" encoding="utf-8"?>
<svg viewBox="3.999 5.9839 40.0083 37.3082" width="40.008px" height="37.308px" xmlns="http://www.w3.org/2000/svg">
  <defs>
        <linearGradient x1="0%" y1="50%" x2="100%" y2="50%" id="linearGradient-1">
            <stop stop-color="#1EE1CB" offset="0%"></stop>
            <stop stop-color="#6321FE" offset="48.3675036%"></stop>
            <stop stop-color="#FF0099" offset="100%"></stop>
        </linearGradient>
    </defs>
  <mask id="mask0_3172_34450" style="mask-type:luminance" maskUnits="userSpaceOnUse" x="0" y="0" width="48" height="48">
    <rect width="48" height="48" fill="white"/>
  </mask>
  <g mask="url(#mask0_3172_34450)" transform="matrix(1, 0, 0, 1, 0, 1.7763568394002505e-15)">
    <path fill-rule="evenodd" clip-rule="evenodd" d="M7.95816 40.2001C7.63235 40.2005 7.30757 40.1636 6.99016 40.0901C5.71152 39.7484 4.64096 38.8745 4.05016 37.6901C3.94538 37.4648 4.00531 37.1972 4.19616 37.0381C8.47416 33.4801 7.34816 28.3201 6.52416 24.5501C6.35816 23.7921 6.20216 23.0781 6.10616 22.4421C5.61209 18.8351 6.73975 15.1944 9.18616 12.4981C12.9926 8.32269 18.3901 5.9557 24.0402 5.98414C24.0758 5.98414 24.1106 5.98754 24.1444 5.99404C29.7289 6.016 35.0523 8.37689 38.8182 12.5081C41.2643 15.2045 42.3919 18.8451 41.8982 22.4521C41.8027 23.0695 41.6523 23.7646 41.4931 24.5005L41.4802 24.5601C40.6562 28.3281 39.5302 33.4881 43.8102 37.0481C44.001 37.2072 44.0609 37.4748 43.9562 37.7001C43.3656 38.8846 42.2949 39.7586 41.0162 40.1001C40.6964 40.1707 40.3696 40.2042 40.0422 40.2001C38.2752 40.0648 36.6064 39.3344 35.3082 38.1281C35.1467 38.0083 35.0639 37.8096 35.0924 37.6105C35.1209 37.4115 35.2561 37.244 35.4447 37.1743C35.6333 37.1045 35.845 37.1436 35.9962 37.2761C37.2358 38.5542 38.9902 39.1976 40.7622 39.0241C41.5854 38.8111 42.299 38.2974 42.7622 37.5841C38.3862 33.6161 39.6022 28.0441 40.4142 24.3261C40.5762 23.5861 40.7282 22.8861 40.8142 22.2881C41.278 18.995 40.24 15.6675 37.9862 13.2221C34.3904 9.28609 29.2953 7.05792 23.9642 7.09014C23.9279 7.09014 23.8925 7.08663 23.8583 7.07992C18.5933 7.09885 13.573 9.32088 10.0182 13.2121C7.76354 15.6571 6.72546 18.985 7.19016 22.2781C7.27198 22.8118 7.40126 23.4229 7.5386 24.0721L7.59016 24.3161C8.40216 28.0341 9.61816 33.6041 5.24416 37.5721C5.70783 38.2856 6.42099 38.8005 7.24416 39.0161C9.01119 39.1806 10.7578 38.5374 11.9962 37.2661C12.1474 37.1336 12.359 37.0945 12.5476 37.1643C12.7362 37.234 12.8714 37.4015 12.8999 37.6005C12.9284 37.7996 12.8456 37.9982 12.6842 38.1181C11.3895 39.3265 9.72357 40.0604 7.95816 40.2001ZM12.9182 24.3281C12.6255 24.3257 12.3863 24.0937 12.3751 23.8012C12.3639 23.5087 12.5845 23.259 12.8762 23.2341C16.9372 22.9154 23.6815 21.8561 26.9132 18.3538C26.9403 18.3143 26.9731 18.2778 27.0112 18.2456C27.4278 17.7772 27.7821 17.266 28.0602 16.7081C28.2028 16.4527 28.521 16.3543 28.7829 16.4847C29.0448 16.6152 29.1581 16.9284 29.0402 17.1961C28.7738 17.7307 28.4475 18.2261 28.0712 18.685C29.7363 20.7834 32.0349 22.2943 34.6302 22.9881C34.8971 23.0583 35.0702 23.3161 35.0342 23.5897C34.9981 23.8634 34.7642 24.0675 34.4882 24.0661C34.4395 24.066 34.391 24.0592 34.3442 24.0461C31.5765 23.3047 29.1192 21.7097 27.3171 19.4961C23.7011 22.9494 17.0373 24.0064 12.9622 24.3261L12.9182 24.3281ZM27.4341 36.2553C27.3696 37.2357 26.5546 38.0111 25.5582 38.0121H22.8922C21.854 38.011 21.0124 37.1703 21.0102 36.1321V35.5321C21.0124 34.494 21.854 33.6532 22.8922 33.6521H25.5582C26.4675 33.6531 27.2257 34.2989 27.4003 35.1569C29.9608 34.8758 32.2347 34.1516 33.9784 33.1367C35.1733 29.6325 35.4177 26.4331 35.4222 26.3621C35.4431 26.06 35.7051 25.8322 36.0072 25.8531C36.3093 25.8741 36.5371 26.136 36.5162 26.4381C36.5115 26.5031 36.319 29.0354 35.4342 32.1182C36.6609 31.0793 37.4183 29.8513 37.5402 28.5381C37.5683 28.2366 37.8356 28.015 38.1372 28.0431C38.4387 28.0713 38.6603 28.3386 38.6322 28.6401C38.4447 30.6423 37.0555 32.4673 34.8804 33.8418C33.2598 38.3673 30.0905 43.2921 23.9722 43.2921H23.7402H23.5082C12.2482 43.2921 10.9782 26.6061 10.9662 26.4361C10.9457 26.134 11.1741 25.8726 11.4762 25.8521C11.7783 25.8317 12.0397 26.06 12.0602 26.3621C12.0702 26.5201 13.2602 42.1961 23.5082 42.1961L23.7402 42.1961H23.7422H23.9722C28.9584 42.1961 31.8011 38.4793 33.4068 34.6471C31.6999 35.4518 29.6642 36.0174 27.4341 36.2553ZM22.8922 34.7501C22.4581 34.7501 22.1062 35.102 22.1062 35.5361V36.1361C22.1073 36.5695 22.4588 36.9201 22.8922 36.9201H25.5582C25.9907 36.919 26.3411 36.5687 26.3422 36.1361V35.5361C26.3422 35.1028 25.9915 34.7512 25.5582 34.7501H22.8922ZM18.2882 27.5331C18.2809 28.1015 18.7338 28.5691 19.3022 28.5801C19.579 28.5828 19.8457 28.4754 20.0433 28.2814C20.241 28.0875 20.3535 27.823 20.3562 27.5461C20.3561 26.9777 19.8971 26.5159 19.3287 26.5124C18.7603 26.5088 18.2955 26.9647 18.2882 27.5331ZM28.9662 28.5801C28.3975 28.5702 27.9437 28.103 27.9502 27.5343C27.9568 26.9657 28.4214 26.5091 28.9901 26.5123C29.5587 26.5156 30.0181 26.9774 30.0182 27.5461C30.0116 28.1215 29.5415 28.5835 28.9662 28.5801Z" fill="url(#linearGradient-1)"/>
  </g>
</svg>"""
    else:
        return """<?xml version="1.0" encoding="utf-8"?>
<svg viewBox="2.2507 1.4963 12.7785 15.0037" width="40.008px" height="37.308px" xmlns="http://www.w3.org/2000/svg">
  <defs>
        <linearGradient x1="0%" y1="50%" x2="100%" y2="50%" id="linearGradient-1">
            <stop stop-color="#1EE1CB" offset="0%"></stop>
            <stop stop-color="#6321FE" offset="48.3675036%"></stop>
            <stop stop-color="#FF0099" offset="100%"></stop>
        </linearGradient>
    </defs>
  <mask id="mask0_3177_36520" style="mask-type:luminance" maskUnits="userSpaceOnUse" x="0" y="0" width="18" height="18">
    <rect width="18" height="18" fill="white"/>
  </mask>
  <g mask="url(#mask0_3177_36520)" transform="matrix(1, 0, 0, 1, -2.220446049250313e-16, 0)">
    <path fill-rule="evenodd" clip-rule="evenodd" d="M5.37542 7.67155C4.90043 7.01125 4.62733 6.19749 4.64394 5.32237C4.68451 3.18359 6.44035 1.47666 8.57942 1.49651C10.7185 1.51636 12.4424 3.25557 12.4432 5.39474C12.4298 6.28444 12.124 7.10128 11.6185 7.75501C11.7812 7.86518 11.9378 7.98409 12.0877 8.11124C12.163 8.17406 12.1908 8.27735 12.1572 8.36945C12.1236 8.46155 12.0358 8.52267 11.9377 8.52224L11.94 8.52449C11.8851 8.52465 11.8319 8.50524 11.79 8.46974C11.6373 8.33993 11.477 8.21942 11.31 8.10883C10.5791 8.85339 9.55693 9.30958 8.43148 9.29474C7.33684 9.26336 6.35973 8.78359 5.67212 8.0358C5.6697 8.03748 5.66724 8.03913 5.66473 8.04074C3.91573 9.12224 2.87173 11.2785 2.72098 14.1157C3.71848 15.2827 5.93923 16.0327 8.42098 16.0327C10.8892 16.0327 13.1707 15.2542 14.1435 14.0865C14.127 13.7992 14.1015 13.5165 14.0685 13.2442C14.0565 13.1608 14.0904 13.0774 14.1573 13.0261C14.2241 12.9748 14.3134 12.9635 14.3909 12.9966C14.4685 13.0296 14.5221 13.102 14.5312 13.1857C14.571 13.4977 14.5995 13.8225 14.616 14.1517C14.6184 14.2077 14.6009 14.2627 14.5665 14.307C13.5225 15.6397 11.1105 16.5 8.41798 16.5C5.77573 16.5 3.39298 15.666 2.32573 14.3722C2.27775 14.328 2.25053 14.2657 2.25073 14.2005V14.1885C2.39064 11.1693 3.49937 8.85753 5.37542 7.67155ZM11.9775 5.39774C11.9774 6.23767 11.6755 7.00771 11.1738 7.60464L11.1713 7.60595C11.118 7.63353 11.0784 7.67996 11.0589 7.73463C10.4404 8.39967 9.56101 8.81922 8.58224 8.82992C6.70128 8.85047 5.15412 7.35338 5.11281 5.47276C5.0715 3.59213 6.55143 2.02855 8.43148 1.96649V1.96574C10.3574 1.93691 11.9434 3.47195 11.9775 5.39774ZM10.9297 10.7595C10.9297 11.8915 11.8474 12.8092 12.9795 12.8092C14.111 12.808 15.028 11.891 15.0292 10.7595C15.0292 9.62744 14.1115 8.70974 12.9795 8.70974C11.8474 8.70974 10.9297 9.62744 10.9297 10.7595ZM11.5155 10.1535C11.7609 9.56167 12.3387 9.17594 12.9795 9.17624V9.17549C13.854 9.17673 14.5623 9.88576 14.5627 10.7602C14.5627 11.401 14.1767 11.9786 13.5847 12.2237C12.9927 12.4689 12.3114 12.3332 11.8584 11.88C11.4054 11.4269 11.2701 10.7454 11.5155 10.1535ZM12.72 11.4555C12.6572 11.4555 12.5971 11.4301 12.5535 11.385L12.144 10.9657C12.0596 10.8728 12.064 10.7297 12.1539 10.642C12.2438 10.5544 12.3869 10.5536 12.4777 10.6402L12.7245 10.893L13.4827 10.1527C13.5757 10.0684 13.7188 10.0728 13.8064 10.1626C13.8941 10.2525 13.8949 10.3956 13.8082 10.4865L12.8827 11.3865C12.8397 11.4301 12.7812 11.4549 12.72 11.4555Z" fill="url(#linearGradient-1)"/>
  </g>
</svg>"""
        
def query_rag_pipeline(query,session_messages,new_context = False):
    data = {
        "query": query,
        "conv_history": session_messages,
        "new_context": new_context
    }

    body = str.encode(json.dumps(data))

    url = os.environ['AZURE_URL']
    # Replace this with the primary/secondary key or AMLToken for the endpoint
    api_key = os.environ['AZURE_API_KEY']
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    # The azureml-model-deployment header will force the request to go to a specific deployment.
    # Remove this header to have the request observe the endpoint traffic rules
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'zephyr-7b-beta-1' }

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        jsonResponse = json.loads(result.decode())
        # print(result)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))
    
    return jsonResponse
            
def setup():
        
    
    allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.
    if "container_client" not in st.session_state:
        container_client = ContainerClient(os.environ['AZURE_BLOB_ACCOUNT_URL'],os.environ['AZURE_BLOB_JPG_CONTAINER'],os.environ['AZURE_BLOB_KEY'])
        st.session_state.container_client = container_client

        container_client = ContainerClient(os.environ['AZURE_BLOB_ACCOUNT_URL'],os.environ['AZURE_BLOB_TEXT_CONTAINER'],os.environ['AZURE_BLOB_KEY'])
        st.session_state.faq_container_client = container_client
    
    st.title('Discovery Bot Chat Demo')
    welcome_msg = "Hello 👋 I am your Discovery Bank chatbot that is able to assist you with queries regarding Discovery Bank."
    with st.chat_message("assistant", avatar=getUserIcon("assistant")):
        st.markdown(welcome_msg)
    
    if "global_btn_key" not in st.session_state:
        st.session_state.global_btn_key = 0
    
    # messages are the messages the user sees, we keep track of everything
    # chat_context is only the chat history we want to pass back
    # setup session state memory
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.chat_context = []
        
    global new_chat_context
    new_chat_context = False
    if len(st.session_state.messages) == 0:
        new_chat_context = True        
    else: 
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar=getUserIcon(message["role"])):
                content = message["content"]
                if "sources" in message:                    
                    st.markdown(content)
                    add_sources(message["sources"])            
                else:
                    st.markdown(content)            
    
def create_button(btn_key,source_file):
    st.session_state.global_btn_key = st.session_state.global_btn_key + 1 
    image_data = get_image_data(source_file)
    st.image(image_data,output_format="JPEG")

    st.download_button(
        key = st.session_state.global_btn_key,
        label="Download Source",
        data=image_data,
        file_name="data_source.jpg",
        mime='image/jpeg'
    )

def create_faq_button(btn_key):
    st.session_state.global_btn_key = st.session_state.global_btn_key + 1 

    faq_data = get_faq_data()
    
    st.download_button(
        key = st.session_state.global_btn_key,
        label="Download FAQS",
        data=faq_data,
        file_name="all_faqs.txt",
        mime='text/txt'
    )
    # st.button(key = btn_key,label = "View Source", on_click = show_user_source,kwargs = {"file_path":source_file})

def get_image_data(file_path):
    file_path_parts =  file_path.split("\\")
    azure_file_path = file_path_parts[1] +'/' + file_path_parts[2]
    try:
        blob_name = st.session_state.container_client.list_blobs(name_starts_with=azure_file_path).next()
    except:
        print(f"No blob found with the file_path {azure_file_path}")
        return
    
    download_stream = st.session_state.container_client.download_blob(blob_name)
    blob_bytes = download_stream.readall()

    with open(file_path_parts[2], "wb") as file:
        file.write(blob_bytes)
        
    image = Image.open(file_path_parts[2])

    buf = BytesIO()
    image.save(buf, format="JPEG")
    byte_im = buf.getvalue()

    return byte_im

def get_faq_data():
    faq_file_path = './faq_blob_download.txt'
    
    if "faqs_read" not in st.session_state:
        st.session_state.faqs_read = True

        container_client = st.session_state.faq_container_client
        blob_generator = container_client.list_blobs()
        
    
        for blob in blob_generator:
            with open(file=faq_file_path, mode="wb") as blob_file:
                print(f"Started downloading {blob}")
                download_stream = container_client.download_blob(blob)
                print(f"File downloaded, streaming blob into {faq_file_path}")
                blob_file.write(download_stream.readall())

    with open(faq_file_path) as file:
        all_faqs= file.readlines()

    s = "\n".join(all_faqs) 
    
    return s

def add_sources(sources):
    for source in sources:
        source_message = source['text'].encode('ascii', errors='ignore').decode().replace("\\n", "")
    
        with st.expander("**Source:** " + source['file'].replace("target-dir\\","")):
            st.markdown(F"**Score:** {source['score']}")
            st.markdown(F"**Extract:** {source_message}")
            
            btn_key = source['id'] + '0'
            
            if source['file'] != 'FAQ_file':
                create_button(btn_key,source['file'])
                #st.session_state.messages.append({"role": "assistant", "content": source_message, "btn_type": "general", "btn_key": source['id'], "source_file": source['file'], "score": source['score']})
                
            else:
                create_faq_button(btn_key)
                #st.session_state.messages.append({"role": "assistant", "content": source_message, "btn_type": "faq", "btn_key": source['id'], "source_file": source['file'], "score": source['score']})
                        

def react_to_message():
                
    # React to user input
    # if prompt := st.chat_input("How can I assist?"):
    #     with st.chat_message("assistant"):
    #         st.markdown("Thanks")
            
    #         for i in range(4):
    #             st.markdown(i)
    #             create_button(i,"target-dir\\discovery-card-miles-terms-and-conditions_parts\\discovery-card-miles-terms-and-conditions_part_7.jpg")
                # st.button(key = i,label = "View Source", on_click = show_user_source,kwargs = {"file_path": "target-dir\discovery-card-miles-terms-and-conditions_parts\discovery-card-miles-terms-and-conditions_part_7.jpg"})
    if prompt := st.chat_input("How can I assist?"):
        
        # Display user message in chat message container
        st.chat_message("user", avatar=getUserIcon("user")).markdown(prompt)
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.chat_context.append({"role": "user", "content": prompt})
        

        result = query_rag_pipeline(prompt,st.session_state.chat_context,new_context = new_chat_context)
        # print(result)
        response = result['response']
        sources = result['sources']
        # source_message = response + '\n'

        
        with st.chat_message("assistant", avatar=getUserIcon("assistant")):
            st.markdown(response)
            st.session_state.chat_context.append({"role": "assistant", "content": response})
            st.session_state.messages.append({"role": "assistant", "content": response, "sources" : sources})

            add_sources(sources)
            
            
                
                # source_message = F"- Source: {source['file']} \n {source['score']} \n {source['text'].encode('ascii', errors='ignore')}\n\n\n"
                # st.markdown(source_message)
                
                
                # # source_message = source_message + F"- Source: {source['file']} \n {source['score']} \n {source['text'].encode('ascii', errors='ignore')}\n\n\n" 
                # if source['file'] != 'FAQ_file':
                #     create_button(source['id'],source['file'])
                #     st.session_state.messages.append({"role": "assistant", "content": source_message, "btn_type": "general", "btn_key": source['id'], "source_file": source['file']})
                # else:
                #     create_faq_button(source['id'])
                #     st.session_state.messages.append({"role": "assistant", "content": source_message, "btn_type": "faq", "btn_key": source['id']})
                    
                        # st.button(,label = "View Source", on_click = show_user_source,kwargs = {"file_path":})
                
            # st.markdown(source_message)

            
        # complete_message = F"{response} + \n\n + {source_message}"
        # # response = f"Echo: {prompt}"
        # # Display assistant response in chat message container
        # with st.chat_message("assistant"):
        #     st.markdown(complete_message)
        
        
        # Add assistant response to chat history

setup()
react_to_message()
# show_user_source("target-dir\discovery-card-miles-terms-and-conditions_parts\discovery-card-miles-terms-and-conditions_part_7.jpg")
# react_to_message()
