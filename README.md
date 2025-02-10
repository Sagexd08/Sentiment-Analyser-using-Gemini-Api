# Sentiment-Analyser-using-Gemini-Api

## Overview
This project is a **Sentiment Analyzer** that utilizes Google's **Gemini API** to analyze the sentiment of text input. It classifies the sentiment into categories such as **Positive, Negative, and Neutral**, providing insights based on text analysis. This project is implemented using **Python** and integrates the **Gemini AI model** for Natural Language Processing (NLP).

## Features
- **Real-time Sentiment Analysis**
- **Integration with Gemini API**
- **Support for Multiple Languages**
- **JSON-formatted Output**
- **Highly Scalable & Lightweight**

## Tech Stack
- **Python** (Primary Language)
- **Google Gemini API** (NLP Model)
- **Jupyter Notebook** (for Testing & Development)

---

## Installation & Setup

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.8+
- `pip` (Python Package Installer)
- An API Key from [Google Gemini AI](https://ai.google.dev/)

### Step 1: Clone the Repository
```bash
git clone https://github.com/Sagexd08/sentiment-analyzer-gemini.git
cd sentiment-analyzer-gemini
```

### Step 2: Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate   # For macOS/Linux
venv\Scripts\activate      # For Windows
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up API Key
Create a `.env` file in the root directory and add:
```
GEMINI_API_KEY=your_api_key_here
```
Or set it as an environment variable:
```bash
export GEMINI_API_KEY=your_api_key_here  # macOS/Linux
set GEMINI_API_KEY=your_api_key_here     # Windows
```

### Step 5: Run the Sentiment Analyzer
```bash
python sentiment_analyzer.py
```

---

## Usage
### CLI Usage
```bash
python sentiment_analyzer.py "I am very happy today!"
```
**Output:**
```
Sentiment: Positive
Confidence Score: 0.92
```

---

## Contributing
1. **Fork** the repository.
2. **Clone** your fork:
   ```bash
   git clone https://github.com/Sagexd08/sentiment-analyzer-gemini.git
   ```
3. **Create a feature branch:**
   ```bash
   git checkout -b feature-branch
   ```
4. **Commit your changes:**
   ```bash
   git commit -m "Add new feature"
   ```
5. **Push the branch:**
   ```bash
   git push origin feature-branch
   ```
6. **Open a Pull Request.**

---

## License
This project is licensed under the **MIT License**.

---

## Author
- **[Sagexd08]** – [GitHub Profile](https://github.com/Sagexd08)

---

## Acknowledgments
- Google Gemini API Team
- Open-source community

