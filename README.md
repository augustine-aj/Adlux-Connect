# Adlux-Connect

## Work in Progress

**This project is currently under development. We're continuously enhancing and refining the Apollo Adlux Hospital RAG Chatbot system to deliver even more accurate, helpful, and seamless user experiences. Stay tuned for future updates!**


The Apollo Adlux Hospital RAG Chatbot system, Built with the Ollama 3.2 LLM model, this chatbot leverages Retrieval-Augmented Generation (RAG) to offer accurate, contextually relevant answers by pulling information from hospital resources and FAQs.

## Introduction

This project provides a transformative solution to healthcare systems by deploying a hospital-based chatbot that utilizes cutting-edge advancements in Artificial Intelligence (AI). By integrating the Retrieval-Augmented Generation (RAG) approach and leveraging powerful local generative AI models such as Llama 3.2, this application delivers fast, accurate, and secure responses, offering a personalized user experience for patients and medical staff alike.

The chatbot is equipped with advanced features like ChromaDB, a vector database for efficient data retrieval, and offers reliable AI-driven responses in a secure, local deployment. It helps bridge the gap in communication by offering easy access to health-related information, medical advice, appointment booking, and other essential services, ensuring users can receive the support they need promptly, without having to wait for human intervention.

## Key Benefits

- **Personalized Assistance:** The chatbot offers tailored responses based on a comprehensive health database containing information on health conditions, symptoms, treatment options, healthcare services, and more. This personalization ensures that each user receives relevant and precise advice.

- **24/7 Availability:** With round-the-clock availability, the chatbot offers instant access to information at any time, reducing patient wait times and improving the overall experience by providing immediate support, no matter the hour.

- **Improved Efficiency for Hospital Staff:** By automating frequent inquiries, appointment scheduling, and delivering general medical information, the chatbot reduces the administrative burden on hospital staff, allowing them to focus on more complex tasks and patient care.

- **Data Security and Compliance:** The AI model, which runs locally, ensures the confidentiality and security of patient data, remaining within the hospital’s secure network and adhering to stringent data protection and privacy regulations.

- **Scalability and Flexibility:** This system is designed to be easily integrable into any hospital environment, regardless of its size. It’s scalable to accommodate future growth and to adapt to the evolving needs of healthcare providers and their patients.
## Features

- **Advanced Chatbot Interaction:** Integrated with Llama 3.2, a state-of-the-art generative model, providing real-time, interactive communication between the system and users.
- **Efficient Data Retrieval:** Uses ChromaDB, a vector database that allows the system to fetch and deliver the most relevant information quickly, enhancing response quality and accuracy.
- **Tailored User Experience:** Personalized interactions designed to cater to specific healthcare inquiries ranging from basic queries to complex medical advice.
- **User Authentication**: Using custom user models (CustomUser) for user management.
- **Chat Session Management**: Chat history with unique session identifiers for seamless interaction tracking.
- **Persistent Data Storage**: Stores user inputs, chatbot responses, and user feedback for long-term reference.
- **Feedback System**: Allows users to rate the chatbot's responses (e.g., Bad, Average, Good, Excellent).
- **Timestamp Handling**: Records session start and end times.
- **Session Title Management**: Dynamically generates and updates session titles.
- **RAG Chatbot Integration**: Retrieval-augmented generation (RAG) using ChromaDB as a vector database.
- **Generative Model**: Llama 3.2, capable of functioning on a local machine, processes requests and generates appropriate responses.
  
## Real-World Example: Hospital-based Chatbot with RAG Approach

This chatbot aims to assist patients by providing real-time responses related to hospital services, medical conditions, available treatments, and doctor appointments. The RAG approach is implemented by storing relevant hospital data (e.g., medical conditions, doctor information, services) as embeddings in ChromaDB. When the user asks a question, the chatbot performs a retrieval task from the vector database and generates a contextual response using the Llama 3.2 model. This setup allows the bot to offer accurate and personalized medical responses, while also keeping healthcare data secure and localized for offline operation.

### How It Works:

1. **Vector Database with ChromaDB**: All important documents and data, including hospital policies, treatments, staff details, patient records, and frequently asked questions, are indexed and stored as vector embeddings in ChromaDB.
2. **RAG Architecture**: When a patient queries the chatbot about symptoms, treatments, or appointment availability, the model searches for relevant vectors in the database (retrieval) and combines them with generative responses based on pre-trained Llama 3.2 outputs to provide a comprehensive and dynamic answer.
3. **Local Deployment**: Since Llama 3.2 runs on a local machine, this system allows sensitive data such as medical information to be kept securely within hospital premises, reducing privacy concerns.

---

## Requirements

### Backend
- **Python 3.9 or above**
- **Django 4.0 or above**
- **PostgreSQL or SQLite** (or any Django-supported database)
- **ChromaDB** (for vector storage)
- **Llama 3.2** (Local Generative Model)

### Frontend
- **HTML, CSS** (Optionally using Django templates for customization)

