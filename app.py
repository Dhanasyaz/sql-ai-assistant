import streamlit as st
from sqlalchemy import create_engine, text
from config import DATABASE_URI
from utills import get_db_schema, call_euri_llm, execute_sql
import speech_recognition as sr
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="SQL Assistant", layout="wide")
st.title("🧠 SQL-Powered Data Retrieval Assistant with Visualizations")


# Database Connection

@st.cache_resource
def get_db_engine():
    return create_engine(DATABASE_URI)

engine = get_db_engine()


# Visualization Function

def create_visualizations(df):
    """Auto-generate visualizations based on data"""
    if df.empty or len(df) == 0:
        return
    
    # Skip visualization for single-cell results
    if df.shape == (1, 1):
        return
    
    # Make a copy to avoid modifying original
    df = df.copy()
    
    # Detect column types
    numeric_cols = df.select_dtypes(include=['int64', 'float64', 'int32', 'float32', 'number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category', 'string']).columns.tolist()
    date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    # Try to detect and convert date columns
    for col in df.columns:
        if col not in date_cols and ('date' in col.lower() or 'month' in col.lower() or 'year' in col.lower() or 'time' in col.lower()):
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                if col not in date_cols:
                    date_cols.append(col)
            except:
                pass
    
    # If no numeric or categorical columns, try to find any usable columns
    if not numeric_cols:
        # Check if any column can be treated as numeric
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                if df[col].notna().any():
                    numeric_cols.append(col)
            except:
                pass
    
    if not categorical_cols:
        # Use non-numeric, non-date columns as categorical
        for col in df.columns:
            if col not in numeric_cols and col not in date_cols:
                categorical_cols.append(col)
    
    # Must have at least one numeric column to visualize
    if not numeric_cols:
        return
    
    st.markdown("---")
    st.subheader("📈 Visualizations")
    
    # Create tabs for different chart types
    tabs = st.tabs(["📊 Main Chart", "📈 Trend/Comparison", "🥧 Distribution", "📉 Analysis"])
    
    # Tab 1: Main Chart (Line/Bar based on data type)
    with tabs[0]:
        try:
            if date_cols and numeric_cols:
                # Time series line chart
                fig = px.line(df, x=date_cols[0], y=numeric_cols[0], 
                             title=f"{numeric_cols[0].replace('_', ' ').title()} Over Time",
                             markers=True)
                fig.update_traces(line_color='#636EFA', line_width=3)
                fig.update_layout(height=450, hovermode='x unified')
                st.plotly_chart(fig, use_container_width=True)
                
            elif categorical_cols and numeric_cols:
                # Bar chart
                # Limit to top 15 for readability
                if len(df) > 15:
                    df_plot = df.nlargest(15, numeric_cols[0])
                else:
                    df_plot = df
                    
                fig = px.bar(df_plot, x=categorical_cols[0], y=numeric_cols[0],
                            title=f"{numeric_cols[0].replace('_', ' ').title()} by {categorical_cols[0].replace('_', ' ').title()}",
                            color=numeric_cols[0],
                            color_continuous_scale='Blues')
                fig.update_layout(height=450, xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
                
            elif len(numeric_cols) >= 2:
                # Scatter plot
                fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1],
                               title=f"{numeric_cols[1]} vs {numeric_cols[0]}",
                               size=numeric_cols[0] if len(df) < 50 else None)
                fig.update_layout(height=450)
                st.plotly_chart(fig, use_container_width=True)
            
            elif len(numeric_cols) == 1:
                # Single numeric column - show bar chart with index
                fig = px.bar(df, y=numeric_cols[0],
                            title=f"{numeric_cols[0].replace('_', ' ').title()}",
                            color=numeric_cols[0],
                            color_continuous_scale='Blues')
                fig.update_layout(height=450)
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.info(f"Could not generate main chart: {str(e)}")
    
    # Tab 2: Trend/Comparison
    with tabs[1]:
        try:
            if date_cols and numeric_cols:
                # Area chart
                fig = px.area(df, x=date_cols[0], y=numeric_cols[0],
                             title=f"{numeric_cols[0].replace('_', ' ').title()} Trend",
                             color_discrete_sequence=['#00CC96'])
                fig.update_layout(height=450)
                st.plotly_chart(fig, use_container_width=True)
                
            elif categorical_cols and numeric_cols:
                # Horizontal bar chart
                df_sorted = df.sort_values(by=numeric_cols[0], ascending=True)
                # Limit to top 15 for readability
                if len(df_sorted) > 15:
                    df_sorted = df_sorted.tail(15)
                    
                fig = px.bar(df_sorted, y=categorical_cols[0], x=numeric_cols[0],
                            orientation='h',
                            title=f"Comparison: {categorical_cols[0].replace('_', ' ').title()}",
                            color=numeric_cols[0],
                            color_continuous_scale='Viridis')
                fig.update_layout(height=450)
                st.plotly_chart(fig, use_container_width=True)
            
            elif len(numeric_cols) >= 2:
                # Line chart comparing two metrics
                fig = go.Figure()
                fig.add_trace(go.Scatter(y=df[numeric_cols[0]], mode='lines+markers', name=numeric_cols[0]))
                fig.add_trace(go.Scatter(y=df[numeric_cols[1]], mode='lines+markers', name=numeric_cols[1]))
                fig.update_layout(title="Metric Comparison", height=450)
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.info(f"Could not generate comparison chart: {str(e)}")
    
    # Tab 3: Distribution
    with tabs[2]:
        try:
            if categorical_cols and numeric_cols and len(df) <= 15:
                # Pie chart
                fig = px.pie(df, names=categorical_cols[0], values=numeric_cols[0],
                            title=f"{numeric_cols[0].replace('_', ' ').title()} Distribution",
                            hole=0.4)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(height=450)
                st.plotly_chart(fig, use_container_width=True)
                
            elif numeric_cols:
                # Histogram
                fig = px.histogram(df, x=numeric_cols[0],
                                 title=f"{numeric_cols[0].replace('_', ' ').title()} Frequency Distribution",
                                 nbins=min(20, len(df)),
                                 color_discrete_sequence=['#EF553B'])
                fig.update_layout(height=450)
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.info(f"Could not generate distribution chart: {str(e)}")
    
    # Tab 4: Analysis
    with tabs[3]:
        try:
            if len(numeric_cols) >= 2 and len(df) > 1:
                # Correlation heatmap
                corr_matrix = df[numeric_cols].corr()
                fig = px.imshow(corr_matrix, 
                              title="Correlation Heatmap",
                              color_continuous_scale='RdBu',
                              text_auto='.2f',
                              aspect="auto")
                fig.update_layout(height=450)
                st.plotly_chart(fig, use_container_width=True)
                
            elif numeric_cols and len(df) > 1:
                # Box plot
                fig = px.box(df, y=numeric_cols[0],
                            title=f"{numeric_cols[0].replace('_', ' ').title()} Distribution Analysis",
                            color_discrete_sequence=['#AB63FA'])
                fig.update_layout(height=450)
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.info(f"Could not generate analysis chart: {str(e)}")


# Sidebar: Database Schema

with st.sidebar:
    st.header("📋 Database Schema")
    schema = get_db_schema(engine)
    st.text_area("Schema Info", schema, height=300)
    
    st.markdown("### 🎤 Tip")
    st.info("Use the microphone button to speak your query in your preferred language!")


# Main Content

col1, col2 = st.columns([4, 1])

with col1:
    st.subheader("🌐 Choose Language for Speech Recognition")
    language_map = {
        "English (US)": "en-US",
        "Hindi (India)": "hi-IN",
        "Tamil": "ta-IN",
        "Telugu": "te-IN",
        "Spanish": "es-ES",
        "French": "fr-FR",
        "German": "de-DE",
        "Chinese (Mandarin)": "zh-CN",
        "Arabic": "ar-SA",
        "Bengali": "bn-IN",
        "Japanese": "ja-JP",
        "Marathi": "mr-IN"
    }
    selected_language = st.selectbox("Choose a language", list(language_map.keys()))
    language_code = language_map[selected_language]

with col2:
    st.write("")
    st.write("")
    st.write("")

# ----------------------------
# Speech Input Section
# ----------------------------
st.subheader("🎙️ Ask Your Question")

col_mic, col_text = st.columns([1, 4])

nl_query = ""

with col_mic:
    if st.button("🎤 Speak", use_container_width=True, type="primary"):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                st.info(f"🎧 Listening in {selected_language}...")
                audio = recognizer.listen(source, timeout=6)

            nl_query = recognizer.recognize_google(audio, language=language_code)
            st.session_state['query'] = nl_query
            st.success(f"✅ You said: {nl_query}")
            
        except sr.UnknownValueError:
            st.error("❌ Sorry, I couldn't understand the audio.")
        except sr.RequestError as e:
            st.error(f"❌ Speech Recognition API error: {e}")
        except Exception as e:
            st.error(f"❌ Error: {e}")

with col_text:
    nl_query = st.text_input(
        "Or type your question here:",
        value=st.session_state.get('query', ''),
        placeholder="e.g., Show me total sales by month"
    )


# Process Query

if nl_query:
    with open("prompt_template.txt") as f:
        template = f.read()
    prompt = template.format(schema=schema, question=nl_query)

    with st.spinner("🧠 Generating SQL using EURI LLM..."):
        sql_query = call_euri_llm(prompt)

    # Show SQL Query
    with st.expander("📝 Generated SQL Query", expanded=True):
        st.code(sql_query, language="sql")

    # Execute Query
    try:
        with st.spinner("⚡ Executing query..."):
            results, columns = execute_sql(engine, sql_query)
        
        if results:
            # Convert to DataFrame
            df = pd.DataFrame(results, columns=columns)
            
            st.subheader("📊 Query Results")
            
            # Show metrics for single values
            if df.shape == (1, 1):
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    value = df.iloc[0, 0]
                    if isinstance(value, (int, float)):
                        st.metric(label=df.columns[0].replace('_', ' ').title(), 
                                value=f"{value:,.2f}")
                    else:
                        st.metric(label=df.columns[0].replace('_', ' ').title(), 
                                value=value)
            else:
                # Show data table
                st.dataframe(df, width='stretch', height=300)
            
            # Generate visualizations
            create_visualizations(df)
            
            # Summary Statistics
            numeric_cols_for_summary = df.select_dtypes(include=['number']).columns.tolist()
            if len(df) > 1 and len(numeric_cols_for_summary) > 0:
                with st.expander("📈 Summary Statistics"):
                    st.dataframe(df.describe(), width='stretch')
        else:
            st.success("✅ Query executed successfully. No data returned.")
            
    except Exception as e:
        st.error(f"❌ Error running query: {e}")
        st.info("💡 Try rephrasing your question or check the SQL query above")


# Footer

st.markdown("---")
