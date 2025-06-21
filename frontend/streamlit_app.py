import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
from datetime import datetime
import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure Streamlit page
st.set_page_config(
    page_title="SEO Content Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API base URL
API_BASE_URL = "http://localhost:8000"

def main():
    st.title("🚀 SEO Content Generator")
    st.markdown("Generate AI-powered SEO content and marketing strategies")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["🏠 Home", "📊 Generate Plan", "📝 Write Article", "📈 Analytics"]
    )
    
    if page == "🏠 Home":
        show_home_page()
    elif page == "📊 Generate Plan":
        show_plan_generation_page()
    elif page == "📝 Write Article":
        show_article_generation_page()
    elif page == "📈 Analytics":
        show_analytics_page()

def show_home_page():
    st.header("Welcome to SEO Content Generator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Features")
        st.markdown("""
        - **Market Research**: AI-powered competitor analysis
        - **SEO Strategy**: Keyword optimization and planning
        - **Content Planning**: Editorial calendar generation
        - **Article Writing**: SEO-optimized content creation
        - **Quality Review**: Grammar and readability analysis
        - **Performance Estimation**: Traffic and ranking predictions
        """)
    
    with col2:
        st.subheader("🚀 Quick Start")
        st.markdown("""
        1. Go to **Generate Plan** to create your SEO strategy
        2. Use **Write Article** for individual content pieces
        3. Check **Analytics** for performance insights
        
        Make sure your API is running on `localhost:8000`
        """)
    
    # API Status Check
    st.subheader("🔗 API Status")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            st.success("✅ API is running properly!")
        else:
            st.error("❌ API is not responding correctly")
    except:
        st.error("❌ Cannot connect to API. Make sure it's running on localhost:8000")

def show_plan_generation_page():
    st.header("📊 Generate SEO Content Plan")
    
    with st.form("business_input_form"):
        st.subheader("Business Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            business_type = st.text_input(
                "Business Type",
                placeholder="e.g., E-commerce, SaaS, Consulting"
            )
            
            product_service = st.text_area(
                "Product/Service Description",
                placeholder="Describe your main products or services"
            )
        
        with col2:
            target_audience = st.text_input(
                "Target Audience",
                placeholder="e.g., Small business owners, Tech entrepreneurs"
            )
            
            niche_keywords = st.text_input(
                "Niche Keywords (comma-separated)",
                placeholder="keyword1, keyword2, keyword3"
            )
        
        content_tone = st.selectbox(
            "Content Tone",
            ["professional", "casual", "technical", "friendly", "authoritative"]
        )
        
        preferred_length = st.slider("Preferred Article Length", 800, 3000, 1500)
        
        submitted = st.form_submit_button("🚀 Generate Plan")
        
        if submitted:
            if all([business_type, product_service, target_audience, niche_keywords]):
                generate_content_plan(
                    business_type, product_service, target_audience,
                    niche_keywords, content_tone, preferred_length
                )
            else:
                st.error("Please fill in all required fields")

def generate_content_plan(business_type, product_service, target_audience, 
                         niche_keywords, content_tone, preferred_length):
    
    with st.spinner("🔍 Researching market and generating plan..."):
        try:
            # Prepare request data
            request_data = {
                "business_type": business_type,
                "product_service": product_service,
                "target_audience": target_audience,
                "niche_keywords": [kw.strip() for kw in niche_keywords.split(",")],
                "content_tone": content_tone,
                "preferred_length": preferred_length
            }
            
            # Make API request
            response = requests.post(
                f"{API_BASE_URL}/generate-plan",
                json=request_data,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()["data"]
                display_content_plan(result)
            else:
                st.error(f"API Error: {response.text}")
                
        except Exception as e:
            st.error(f"Error generating plan: {str(e)}")

def display_content_plan(result):
    st.success("✅ Content plan generated successfully!")
    
    # Market Research Results
    st.subheader("🔍 Market Research")
    research = result["research"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Trending Keywords:**")
        for keyword in research["trending_keywords"]:
            st.write(f"• {keyword}")
    
    with col2:
        st.write("**Search Volume Data:**")
        volume_df = pd.DataFrame(
            list(research["search_volume_data"].items()),
            columns=["Keyword", "Volume"]
        )
        st.bar_chart(volume_df.set_index("Keyword"))
    
    # SEO Strategy
    st.subheader("🎯 SEO Strategy")
    strategy = result["strategy"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Primary Keywords:**")
        for keyword in strategy["primary_keywords"]:
            st.write(f"• {keyword}")
    
    with col2:
        st.write("**Suggested Article Titles:**")
        for i, title in enumerate(strategy["suggested_titles"], 1):
            st.write(f"{i}. {title}")
    
    # Content Calendar
    st.subheader("📅 Content Calendar")
    plan = result["plan"]
    
    calendar_df = pd.DataFrame(plan["content_schedule"])
    st.dataframe(calendar_df, use_container_width=True)
    
    # Store plan in session state for later use
    st.session_state["content_plan"] = result

def show_article_generation_page():
    st.header("📝 Generate SEO Article")
    
    # Check if we have a content plan
    if "content_plan" in st.session_state:
        st.info("💡 You can use titles from your generated content plan or create custom articles")
        
        plan_titles = st.session_state["content_plan"]["strategy"]["suggested_titles"]
        use_plan_title = st.checkbox("Use title from content plan")
        
        if use_plan_title:
            selected_title = st.selectbox("Select title from plan:", plan_titles)
        else:
            selected_title = None
    else:
        selected_title = None
        use_plan_title = False
    
    with st.form("article_generation_form"):
        if use_plan_title:
            title = selected_title
            st.write(f"**Selected Title:** {title}")
        else:
            title = st.text_input(
                "Article Title",
                placeholder="Enter your article title"
            )
        
        keywords = st.text_input(
            "Target Keywords (comma-separated)",
            placeholder="keyword1, keyword2, keyword3"
        )
        
        content_type = st.selectbox(
            "Content Type",
            ["blog_post", "how_to_guide", "listicle", "product_review", "comparison"]
        )
        
        submitted = st.form_submit_button("✍️ Generate Article")
        
        if submitted:
            if title and keywords:
                generate_article(title, keywords, content_type)
            else:
                st.error("Please provide title and keywords")

def generate_article(title, keywords, content_type):
    with st.spinner("✍️ Writing your SEO-optimized article..."):
        try:
            keyword_list = [kw.strip() for kw in keywords.split(",")]
            
            # Make API request
            response = requests.post(
                f"{API_BASE_URL}/generate-article",
                json={
                    "title": title,
                    "keywords": keyword_list,
                    "content_type": content_type
                },
                timeout=180
            )

            
            if response.status_code == 200:
                result = response.json()["data"]
                display_article_result(result)
            else:
                st.error(f"API Error: {response.text}")
                
        except Exception as e:
            st.error(f"Error generating article: {str(e)}")

def display_article_result(result):
    st.success("✅ Article generated successfully!")
    
    article = result["article"]
    quality_report = result["quality_report"]
    performance_estimate = result["performance_estimate"]
    
    # Article Preview
    st.subheader("📄 Generated Article")
    
    with st.expander("Article Content", expanded=True):
        st.write(f"**Title:** {article['title']}")
        st.write(f"**Meta Description:** {article['meta_description']}")
        st.write(f"**Word Count:** {article['word_count']}")
        st.write(f"**Keywords:** {', '.join(article['keywords'])}")
        
        st.markdown("---")
        st.markdown(article['content'])
    
    # Quality Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔍 Quality Analysis")
        st.metric("SEO Score", f"{article['seo_score']:.1f}/100")
        st.metric("Grammar Score", f"{quality_report['grammar_score']:.1f}/100")
        st.metric("Readability Score", f"{quality_report['readability_score']:.1f}/100")
        st.metric("Plagiarism Risk", quality_report['plagiarism_risk'])
    
    with col2:
        st.subheader("📈 Performance Estimate")
        st.metric("Estimated Ranking", f"#{performance_estimate['estimated_ranking']}")
        st.metric("Traffic Potential", f"{performance_estimate['traffic_potential']} visits/month")
        st.metric("Competition Level", performance_estimate['competition_level'])
        st.metric("Success Probability", f"{performance_estimate['success_probability']:.1f}%")
    
    # Keyword Density Analysis
    if quality_report['keyword_density']:
        st.subheader("📊 Keyword Density")
        density_df = pd.DataFrame(
            list(quality_report['keyword_density'].items()),
            columns=["Keyword", "Density %"]
        )
        st.bar_chart(density_df.set_index("Keyword"))
    
    # Suggestions
    if quality_report['suggestions']:
        st.subheader("💡 Improvement Suggestions")
        for suggestion in quality_report['suggestions']:
            st.write(f"• {suggestion}")

def show_analytics_page():
    st.header("📈 Analytics Dashboard")
    
    if "content_plan" not in st.session_state:
        st.warning("⚠️ No content plan found. Please generate a plan first.")
        return
    
    st.subheader("📊 Content Plan Overview")
    
    plan = st.session_state["content_plan"]["plan"]
    strategy = st.session_state["content_plan"]["strategy"]
    research = st.session_state["content_plan"]["research"]
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Planned Articles", len(plan["content_schedule"]))
    
    with col2:
        st.metric("Target Keywords", len(strategy["primary_keywords"]))
    
    with col3:
        avg_volume = sum(research["search_volume_data"].values()) / len(research["search_volume_data"])
        st.metric("Avg Search Volume", f"{avg_volume:.0f}")
    
    with col4:
        st.metric("Content Types", len(plan["content_types"]))
    
    # Content Calendar Visualization
    st.subheader("📅 Content Calendar")
    
    calendar_df = pd.DataFrame(plan["content_schedule"])
    calendar_df["date"] = pd.to_datetime(calendar_df["date"])
    
    # Content type distribution
    col1, col2 = st.columns(2)
    
    with col1:
        content_type_counts = calendar_df["content_type"].value_counts()
        fig = px.pie(
            values=content_type_counts.values,
            names=content_type_counts.index,
            title="Content Type Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Timeline view
        fig = px.timeline(
            calendar_df,
            x_start="date",
            x_end="date",
            y="content_type",
            color="content_type",
            title="Content Publishing Timeline"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Keyword Analysis
    st.subheader("🔑 Keyword Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Search Volume by Keyword**")
        volume_df = pd.DataFrame(
            list(research["search_volume_data"].items()),
            columns=["Keyword", "Volume"]
        )
        volume_df = volume_df.sort_values("Volume", ascending=True)
        fig = px.bar(volume_df, x="Volume", y="Keyword", orientation="h")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("**Keyword Difficulty Scores**")
        difficulty_df = pd.DataFrame(
            list(research["difficulty_scores"].items()),
            columns=["Keyword", "Difficulty"]
        )
        fig = px.scatter(
            difficulty_df,
            x="Difficulty",
            y="Keyword",
            size=[research["search_volume_data"].get(kw, 100) for kw in difficulty_df["Keyword"]],
            color="Difficulty",
            title="Keyword Difficulty vs Volume"
        )
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()