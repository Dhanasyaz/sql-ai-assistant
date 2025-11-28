# 🧠 SQL AI Assistant with Voice & Visualizations

An intelligent SQL query assistant that converts natural language (text or speech) into SQL queries and automatically generates beautiful visualizations. Ask questions about your data in plain English, Hindi, Tamil, or 10+ other languages!

<img width="1915" height="920" alt="image" src="https://github.com/user-attachments/assets/add5dc94-2873-4479-bc22-6695e4edae79" />
<img width="1920" height="921" alt="image" src="https://github.com/user-attachments/assets/5e863490-190c-42f9-90bb-e840fb539a3b" />


## ✨ Features

### 🎤 **Multi-Language Voice Input**
- Speak your queries in 12+ languages (English, Hindi, Tamil, Telugu, Spanish, French, etc.)
- Real-time speech-to-text conversion
- Or type your questions manually

### 🤖 **AI-Powered SQL Generation**
- Converts natural language to SQL using EURI LLM
- Understands complex queries
- Shows generated SQL for transparency

### 📊 **Automatic Visualizations**
- **4 types of charts** automatically generated:
  - 📈 Line/Bar Charts - Trends and comparisons
  - 📉 Area/Horizontal Bars - Alternative views
  - 🥧 Pie/Histogram Charts - Distributions
  - 🔥 Heatmaps/Box Plots - Statistical analysis
- Smart chart selection based on data type
- Interactive Plotly visualizations

### 📈 **Data Analysis**
- Summary statistics
- Correlation analysis
- Data tables with results
- Metric displays for single values

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database (we use Neon)
- EURI API key -> any llm api keys in your case

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/sql-ai-assistant.git
cd sql-ai-assistant
```

2. **Create virtual environment**
```bash
python -m venv sqlaienv
source sqlaienv/bin/activate  # On Windows: sqlaienv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory:

```env
EURI_API_KEY=your_euri_api_key_here
DATABASE_URI=postgresql://user:password@host/database?sslmode=require
```

5. **Create prompt template**

Create `prompt_template.txt`:

```text
You are an expert PostgreSQL SQL query generator.

Database Schema:
{schema}

User Question: {question}

Generate ONLY valid PostgreSQL syntax without explanation.
```

6. **Run the application**
```bash
streamlit run app.py
```

## 📁 Project Structure

```
sql-ai-assistant/
├── app.py                  # Main Streamlit application
├── config.py              # Configuration and environment variables
├── utills.py              # Utility functions (DB schema, LLM calls, SQL execution)
├── prompt_template.txt    # LLM prompt template
├── .env                   # Environment variables (not in git)
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── sample_data.sql       # Sample database schema and data
```

## 🗄️ Database Setup

The project includes sample sales data. To set it up:

1. Go to [Neon Console](https://console.neon.tech)
2. Create a new database
3. Run the SQL from `sample_data.sql` in the SQL Editor
4. Copy the connection string to your `.env` file

Otherwise, you can use whichever database setup is most suitable for you.
### Sample Database Schema

- **products** - Product catalog (name, category, price)
- **customers** - Customer information (name, email, location)
- **sales** - Sales transactions (date, amount, quantities)

## 💡 Usage Examples

### Text Queries
```
"Show me total sales by month"
"Top 5 customers by revenue"
"What are the best selling products?"
"Sales by country"
"Revenue trend over time"
```

### Voice Queries
1. Click the 🎤 microphone button
2. Speak your question in your preferred language
3. Watch it convert to SQL and generate visualizations!

## 📦 Dependencies

```
streamlit>=1.28.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
python-dotenv>=1.0.0
pandas>=2.0.0
plotly>=5.18.0
SpeechRecognition>=3.10.0
PyAudio>=0.2.13
requests>=2.31.0
```

## 🛠️ Configuration

### EURI LLM Settings
Edit `config.py` to customize:
- `MODEL_NAME` - AI model to use
- `EURI_API_URL` - API endpoint

### Speech Recognition Languages
Supported languages in the app:
- English (US)
- Hindi (India)
- Tamil, Telugu, Marathi
- Spanish, French, German
- Chinese, Japanese, Arabic
- And more!


## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - Web framework
- [Plotly](https://plotly.com/) - Visualization library
- [EURI AI](https://euron.one/) - LLM provider
- [Neon](https://neon.tech/) - PostgreSQL database
- [SpeechRecognition](https://github.com/Uberi/speech_recognition) - Voice input


## 🐛 Known Issues

- PyAudio installation might require additional system dependencies on some platforms
- Speech recognition requires an active internet connection
- Large datasets may take longer to visualize

## 🔮 Future Enhancements

- [ ] Export results to CSV/Excel
- [ ] Save favorite queries
- [ ] Query history
- [ ] More chart types
- [ ] Custom database connections via UI
- [ ] Dark mode support

---

Made with ❤️ using Streamlit, SQLAlchemy, and AI
