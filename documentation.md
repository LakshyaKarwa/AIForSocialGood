# Project Documentation

## 1. Project Overview

### 1.1 Project Statement
- **Problem Statement**: Describe the primary problem or challenge that the project aims to address.
- **Objectives**: List the key objectives of the project.
- **Target Audience**: Define who the intended beneficiaries or users are.

Problem Statement
India is experiencing a significant mental health crisis, particularly in rural and low-income communities, where access to mental health services is severely limited. Many individuals, such as farmers facing economic distress, lack understanding of English and are in urgent need of support, yet they cannot access affordable care. Additionally, the deaf and hard-of-hearing population suffers from a lack of resources tailored to their communication needs. Despite advancements in global technology for various languages, there remains a critical gap in resources for these underserved populations, highlighting the urgent need for effective solutions that address their mental health and communication challenges.

Objectives
1. Provide Accessible Mental Health Support
2. Inclusive Design: Ensure the platform is accessible to diverse linguistic and disability groups
4. Scalable Solution: Create a scalable model that can expand to include additional regional languages and mental health support systems.
5. Bridge Language Gaps: Facilitate seamless communication by bridging language barriers between other languages and English, while providing a much-needed platform for the underserved communities.

Target Audience
1. Low-Income and Rural Populations: Individuals who have limited access to mental health services, particularly in rural areas where services are scarce and travel is difficult.
2. Farmers and Economically Stressed Communities: People facing severe socio-economic pressures, including farmers who are at high risk of mental health issues and suicides.
3. General Population in Need of Mental Health Support: People across India who require accessible, culturally sensitive mental health advice in their local languages.

This project aims to tackle the critical gaps in mental health accessibility, especially for those most marginalized, by providing a scalable, inclusive, and language-agnostic solution.

### 1.2 Proposed Solution
- **Solution Overview**: Provide a summary of the proposed solution.
- **Key Features**: Highlight the main features of the solution.
- **Expected Impact**: Describe the anticipated outcomes and impacts of the solution.

Solution Overview
The proposed solution is an AI-powered platform designed to deliver accessible mental health support to underrepresented communities in India. The platform accepts inputs in any language, translates them into English for analysis, generates personalized mental health advice, and then translates the advice back into the original language which was spoken by the user. This enables individuals from rural, low-income backgrounds and the deaf and hard-of-hearing community to access critical mental health resources in their native languages, while utilizing India’s affordable internet infrastructure.

Key Features

1. Speech-to-Text:
Converts speech in any language into text using speech recognition technology.

2. Multilingual Translation:
Translates Hindi text to English using a translation model, enabling the system to process the content effectively for advice generation.
Converts the generated advice from English back into the originally used language, ensuring users receive support in their native language.

3. AI-Powered Mental Health Advice:
An AI-based engine analyzes the input and provides tailored mental health advice based on the user's problem, using a mental health knowledge base or support system.

4. Text-to-Speech:
For the users, the advice is delivered as natural-sounding speech using Text-to-Speech (TTS) technology, in their native language.

5. Accessible and Scalable Design:
The platform is lightweight, operates efficiently even on low-cost devices, and is scalable to include additional regional languages or mental health features.

Expected Impact

By providing mental health support in native languages, the platform bridges the gap for millions of individuals in rural and low-income communities who currently lack access to mental health care.
Offering timely and culturally relevant advice, the solution aims to reduce stress, anxiety, and other mental health issues, particularly in high-risk groups like farmers, potentially contributing to a decline in cases of farmer suicides.
By making mental health care more accessible and normalizing seeking help through digital means, the platform could contribute to greater awareness and reduced stigma around mental health in India.
This solution leverages AI to create a scalable, inclusive mental health tool that provides meaningful support to those most in need, making a significant societal impact.

### 1.3 Technical Aspects

- **Programming Languages**: Python for Development (entirely)
- **Frameworks and Libraries**: Tkinter for Front end, SpeechRecognition - for audio input, SpeechBrain - for language detection, Deep Translator for translation, gTTS for google text-to-speech, Google's Generative AI for the model API


## 2. Documentation of AI Tools Used

### 2.1 Overview of AI Tools
Tool Name: 
1. ChatGPT
2. Amazon Q - IDE code completion
3. MetaAI - ASL/ISL understanding
4. Gemini - Mental Health Chat responses
5. Co-pilot - IDE code completion
6. HuggingChat - Transformer model implementation for ASL Sign Recognition

### 2.2 Application of AI Tools

ChatGPT: ChatGPT was used to assist with brainstorming. While the team had core ideas of what we could implement based on our skillset, we used GPT to suggest real life applications of the ideas. We gave it idea specific prompts and goals like low resource ideas etc. and build on the suggestions.
We also used it to help in coding. Since, it is the most available and accessible tool

Copilot: autocompletion of code and code suggestions. modifications of code which were suggested by the tool. since copilot is being used widely and its free to use on a student account.




### 2.3 Total use of AI Tools
- **Arhant Arora-- 65%**: Used chatGPT for parts of code generation.
- **Lakshya Karwa-- 65%**: Used chatGPT to understand American and Indian Sign Language and gather dataset reources from the same, utilized copilot for auto completion of code/suggestions. Used Amazon Q for defining training classes in pytorch.
- **Manav Chaudhary-- 55%**: Used ChatGPT for code generation, help with code for speech recognition library usage. Used Gemini for instruction tuning
- **Siya Gupta-- 60%**: Used ChatGPT for ideation, documentation and presentation and speech recognition library for the google translation API for Hindi to English text.