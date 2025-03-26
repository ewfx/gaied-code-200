#Architecture Diagram

## Overview
This document provides an overview of the system architecture. The architecture diagram showcases the flow of data and interactions between different components of the system, highlighting the processing pipeline from user input to final output.

## Components
The architecture consists of the following key components:

1. **User Email**: Entry point where users send their emails or data for processing.

2. **Request Router**: Routes incoming user requests to the appropriate processing module based on the content type or context.

3. **Data Preprocessing**: Cleans and preprocesses incoming data to remove noise and ensure consistency.

4. **Data Cleaning**: Performs further data sanitization, handling issues such as formatting and data integrity.

5. **Text Parsing Service**: Processes and analyzes structured text data from files (e.g., CSV, JSON, plain text).

6. **OCR Module**: Extracts text from unstructured files like PDFs and DOCs, using OCR technologies to convert them into text format.

7. **Data Enrichment Service**: Enhances data with additional context or metadata to support downstream analysis.

8. **Llama 3 via Ollama**: Uses advanced machine learning models for processing and analyzing enriched data. This module performs core analytics and decision-making.

9. **Database: Supabase PostgreSQL**: Stores processed data and intermediate results, enabling efficient querying and retrieval.

10. **Content Prioritization Layer**: Applies business logic and prioritization rules to the processed data to rank or filter content.

11. **Rules Configuration (rules.json)**: A configuration file that contains the rules used by the prioritization layer for applying business logic.

12. **Gradio UI**: A user interface for visualizing and interacting with processed results.

## Data Flow
1. Users send data through emails which are routed by the **Request Router**.
2. Data undergoes **Preprocessing** and **Cleaning** to ensure it is in the proper format.
3. Depending on the file type, data is sent to either the **Text Parsing Service** or **OCR Module** for text extraction.
4. **Data Enrichment Service** enhances the parsed or extracted data with additional information.
5. Processed data is analyzed using **Llama 3 via Ollama**.
6. Analyzed data is stored in **Supabase PostgreSQL** for future reference and is also made accessible through the **Gradio UI**.
7. The **Content Prioritization Layer** applies predefined rules to rank or filter the output.


