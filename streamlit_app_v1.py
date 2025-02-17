{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "53504f3d-3c54-43eb-9350-8a6b4838bc64",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "import replicate\n",
    "import os\n",
    "\n",
    "# App title\n",
    "st.set_page_config(page_title=\"🦙💬 Llama 2 Chatbot\")\n",
    "\n",
    "# Replicate Credentials\n",
    "with st.sidebar:\n",
    "    st.title('🦙💬 Llama 2 Chatbot')\n",
    "    if 'REPLICATE_API_TOKEN' in st.secrets:\n",
    "        st.success('API key already provided!', icon='✅')\n",
    "        replicate_api = st.secrets['REPLICATE_API_TOKEN']\n",
    "    else:\n",
    "        replicate_api = st.text_input('Enter Replicate API token:', type='password')\n",
    "        if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):\n",
    "            st.warning('Please enter your credentials!', icon='⚠️')\n",
    "        else:\n",
    "            st.success('Proceed to entering your prompt message!', icon='👉')\n",
    "\n",
    "    # Rest of your sidebar code...\n",
    "\n",
    "os.environ['REPLICATE_API_TOKEN'] = replicate_api\n",
    "\n",
    "# Define SessionState class\n",
    "class SessionStateData:\n",
    "    def __init__(self, **kwargs):\n",
    "        for key, val in kwargs.items():\n",
    "            setattr(self, key, val)\n",
    "\n",
    "# Initialize session state\n",
    "def init_session_state():\n",
    "    session_state = SessionStateData(messages=[{\"role\": \"assistant\", \"content\": \"How may I assist you today?\"}])\n",
    "    return session_state\n",
    "\n",
    "session_state = init_session_state()\n",
    "\n",
    "# Display or clear chat messages\n",
    "for message in session_state.messages:\n",
    "    with st.chat_message(message[\"role\"]):\n",
    "        st.write(message[\"content\"])\n",
    "\n",
    "def clear_chat_history():\n",
    "    session_state.messages.clear()\n",
    "    session_state.messages.append({\"role\": \"assistant\", \"content\": \"How may I assist you today?\"})\n",
    "\n",
    "st.sidebar.button('Clear Chat History', on_click=clear_chat_history)\n",
    "\n",
    "# Function for generating LLaMA2 response\n",
    "@st.cache(allow_output_mutation=True)\n",
    "def generate_llama2_response(prompt_input):\n",
    "    string_dialogue = \"You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'.\"\n",
    "    for dict_message in session_state.messages:\n",
    "        if dict_message[\"role\"] == \"user\":\n",
    "            string_dialogue += \"User: \" + dict_message[\"content\"] + \"\\n\\n\"\n",
    "        else:\n",
    "            string_dialogue += \"Assistant: \" + dict_message[\"content\"] + \"\\n\\n\"\n",
    "    output = replicate.run(llm, \n",
    "                           input={\"prompt\": f\"{string_dialogue} {prompt_input} Assistant: \",\n",
    "                                  \"temperature\": temperature, \"top_p\": top_p, \"max_length\": max_length, \"repetition_penalty\": 1})\n",
    "    return output\n",
    "\n",
    "# User-provided prompt\n",
    "if prompt := st.chat_input(disabled=not replicate_api):\n",
    "    session_state.messages.append({\"role\": \"user\", \"content\": prompt})\n",
    "    with st.chat_message(\"user\"):\n",
    "        st.write(prompt)\n",
    "\n",
    "# Generate a new response if the last message is not from the assistant\n",
    "if session_state.messages[-1][\"role\"] != \"assistant\":\n",
    "    with st.chat_message(\"assistant\"):\n",
    "        with st.spinner(\"Thinking...\"):\n",
    "            response = generate_llama2_response(prompt)\n",
    "            placeholder = st.empty()\n",
    "            full_response = ''\n",
    "            for item in response:\n",
    "                full_response += item\n",
    "                placeholder.markdown(full_response)\n",
    "            placeholder.markdown(full_response)\n",
    "    message = {\"role\": \"assistant\", \"content\": full_response}\n",
    "    session_state.messages.append(message)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8dd395bc-f352-4ea9-9ecb-33e1e67b9488",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
