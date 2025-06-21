# 🚀 SEO Content Generator

AI-powered SEO content generation and planning system built with LangChain, FastAPI, and Streamlit.

## 🌟 Features

- **Market Research Agent**: Analyzes competitors and trends
- **SEO Strategist Agent**: Optimizes keyword selection and strategy
- **Content Planner Agent**: Creates editorial calendars
- **Blog Writer Agent**: Generates SEO-optimized articles
- **Quality Reviewer Agent**: Analyzes content quality and readability
- **Performance Estimator Agent**: Predicts ranking and traffic potential

## 🔧 Installation

1. **Clone the repository**
```bash
git clone <repository_url>
cd seo-content-generator
```

2. **Create environment file**
```bash
cp .env.example .env
```

Edit `.env` with your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
SERP_API_KEY=your_serp_api_key_here  # Optional
PORT=8000
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

**Option 1: Run everything with one command**
```bash
python run.py
```

**Option 2: Run components separately**

Start API server:
```bash
cd api
python main.py
```

Start frontend (in another terminal):
```bash
cd frontend
streamlit run streamlit_app.py
```

## 📁 Project Structure

```
seo-content-generator/
├── config/
│   └── settings.py          # Configuration settings
├── models/
│   └── schemas.py           # Pydantic models
├── agents/
│   ├── base_agent.py        # Base agent class
│   ├── market_research_agent.py
│   ├── seo_strategist_agent.py
│   ├── content_planner_agent.py
│   ├── blog_writer_agent.py
│   ├── quality_reviewer_agent.py
│   └── performance_estimator_agent.py
├── workflow/
│   └── seo_workflow.py      # Main workflow orchestration
├── api/
│   └── main.py              # FastAPI application
├── frontend/
│   └── streamlit_app.py     # Streamlit UI
├── requirements.txt
├── .env.example
├── run.py                   # Main runner script
└── README.md
```

## 🔌 API Endpoints

- `POST /generate-plan` - Generate complete SEO content plan
- `POST /generate-article` - Generate single article with analysis
- `POST /evaluate-content` - Evaluate existing content quality
- `GET /health` - Health check

## 🌐 Frontend Features

- **Home**: Overview and API status
- **Generate Plan**: Create comprehensive SEO strategy
- **Write Article**: Generate individual articles
- **Analytics**: View performance metrics and insights

## 🔮 Future Extensions

This project is designed to be easily extensible:

1. **Database Integration**: Add MongoDB/PostgreSQL for data persistence
2. **Advanced APIs**: Integrate real SEO tools (Ahrefs, SEMrush)
3. **User Management**: Add authentication and user accounts
4. **Scheduling**: Add automated content publishing
5. **Analytics**: Real website performance tracking
6. **Team Collaboration**: Multi-user content planning

## 📝 Usage Examples

### Generate Content Plan
```python
business_input = {
    "business_type": "E-commerce",
    "product_service": "Sustainable fashion marketplace",
    "target_audience": "Eco-conscious millennials",
    "niche_keywords": ["sustainable fashion", "eco-friendly clothing"]
}
```

### Generate Article
```python
article_data = {
    "title": "10 Best Sustainable Fashion Brands in 2024",
    "keywords": ["sustainable fashion", "eco-friendly brands"],
    "content_type": "listicle"
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

For issues and questions:
1. Check the README
2. Review API documentation
3. Open an issue on GitHub

---

**Happy Content Creating! 🚀**