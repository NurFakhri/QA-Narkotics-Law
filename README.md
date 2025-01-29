# QA Model for Legal Case Dataset

## Table of Contents
1. [Project Overview](#project-overview)
2. [Dataset](#dataset)
    - [Crawling](#crawling)
    - [Technologies](#technologies)
3. [Dataset Processing](#dataset-processing)
4. [Build Model](#build-model)
    - [API OpenAI](#api-openai)
    - [Generate Answer and Question](#generate-answer-and-question)
    - [Embedding](#embedding)
    - [Cosine Similarity](#cosine-similarity)

## Project Overview
The goal of this project is to build a Question-Answering (QA) system that leverages a legal case dataset to answer legal questions. This project applies Natural Language Processing (NLP) techniques to build a system that can automatically answer questions based on legal cases data, such as verdict, evidence, and context.

### Purpose:
- Automate the process of answering legal-related questions.
- Provide an efficient way to query legal datasets.
- Help legal professionals or researchers retrieve information more effectively.

### Objectives:
- Build a QA system using machine learning techniques.
- Implement an AI-powered solution to extract relevant information from legal case texts.

## Dataset
This dataset consists of legal case data, including verdicts, evidence, and related contextual information. We have crawled data from various legal resources to build this dataset.

### Crawling:
- The dataset was crawled from legal websites using web scraping techniques.
- Key information such as verdicts (`amar_putusan`), evidence (`bukti`), and case context were extracted.
- Scraping was done using Python libraries like `requests` and `BeautifulSoup` to extract data in structured format.

### Technologies:
- Python libraries such as `requests`, `BeautifulSoup`, and `pandas` were used for scraping and data processing.

## Dataset Processing
The dataset was pre-processed to make it suitable for training the QA model. The processing steps included:

1. **Text Cleaning**: Removing unwanted characters, special symbols, and normalizing the text.
2. **Tokenization**: Text data was tokenized to convert text into tokens that can be used by NLP models.
3. **Create Context**: 
   - In this step, two key columns—**`amar_putusan`** (verdict) and **`bukti`** (evidence)—were combined to create a context that provides the full background information for each legal case. 
   - The context was built by concatenating the case verdict (`amar_putusan`) with relevant evidence details (`bukti`). This ensures that the model has access to both the outcome and the supporting evidence when answering questions related to the case.
   - The combined context serves as the input for the question-answering model, allowing it to understand the case's decision in the broader legal context and generate more accurate and relevant answers.

## Build Model

### API OpenAI
For the question-answering part of the system, OpenAI's GPT models were used to generate responses. The OpenAI API was integrated into the model pipeline to provide powerful NLP capabilities. (for alternative, you can use Google AI studio and Groq)

### Generate Answer and Question
- The model generates answers based on the context provided in legal cases.
- The system is able to generate relevant questions for a given legal case text.

### Embedding
- Sentence embeddings were used to represent the legal case data as vectors. These vectors provide a numerical representation of the text that can be used to calculate similarities and identify relevant case data.
- Pre-trained models like Sentence-BERT were used to generate the embeddings for both questions and legal case texts.

### Cosine Similarity
- Cosine similarity is used to compare the similarity between the query (question) and the case texts.
- The cosine similarity score is used to identify the most relevant answers based on the given input question.
