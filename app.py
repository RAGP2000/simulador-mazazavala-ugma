import streamlit as st
import json
import io
from gtts import gTTS
from duckduckgo_search import DDGS
from openai import OpenAI

# 1. Configuración de la página y Diseño Visual Premium
st.set_page_config(page_title="Simulador BCV - Maza Zavala", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main { background-color: #0b101d; color: #f1f5f9; }
    h1, h2, h3 { color: #f59e0b !important; font-family: 'Courier New', Courier, monospace; }
    .stSlider > div > div > div { background-color: #f59e0b; }
    .metric-box { background-color: #0f172a; border: 1px solid #1e293b; padding: 15px; border-radius: 10px; border-left: 4px solid #f59e0b; margin-bottom: 15px;}
    .alert-box { background-color: #450a0a; border: 1px solid #7f1d1d; padding: 15px; border-radius: 10px; border-left: 4px solid #ef4444; margin-top: 20px;}
    </style>
""", unsafe_allow_html=True)

# 2. Encabezado de la Aplicación
st.markdown("<h1>🏛️ Directorio Extraordinario del BCV</h1>", unsafe_allow_html=True)
st.markdown("### Asesor Artificial Maza Zavala (Conexión LLaMA 3.1 y Grounding Web Libre)")

# 3. Panel Lateral: Captura de Datos
with st.sidebar:
    st.header("Mesa Técnica")
    st.caption("Ajuste los parámetros para mitigar el Pass-Through (ERPT)")
    
    tipo_cambio = st.slider("1. Tipo de Cambio Objetivo (Bs/USD)", 25.0, 120.0, 45.5, step=0.1)
    intervencion = st.slider("2. Intervención Semanal (M$ USD)", 10, 300, 80, step=5)
    encaje = st.number_input("3. Encaje Legal (%)", min_value=10, max_value=100, value=73)
    tasa = st.number_input("4. Tasa de Interés (%)", min_value=5, max_value=200, value=40)
    
    fogade = st.selectbox("5. Cobertura FOGADE", [
        "Límite Oficial Vigente (Bs. 15,000)",
        "Garantía Extraordinaria Aumentada (Bs. 100,000)",
        "Ajuste de Cobertura en Divisas ($1,000 USD)"
    ])
    
    justificacion = st.text_area("6. Justificación Técnica (Modelo Leo Butler)", 
                                 "Buscamos anclar las expectativas mediante la absorción de liquidez excedentaria...")
    
    submit_btn = st.button("Someter Decreto a Maza Zavala", use_container_width=True)

# 4. Lógica de IA y Procesamiento
if submit_btn:
    with st.spinner("🔍 Realizando búsqueda en tiempo real y estructurando dictamen..."):
        try:
            # A. Búsqueda en Internet Autónoma (DuckDuckGo)
            try:
                resultados = DDGS().text("tipo de cambio oficial BCV hoy reservas internacionales Venezuela precio crudo Merey", max_results=3)
                contexto_web = "\n".join([res['body'] for res in resultados])
            except Exception:
                contexto_web = "Alta volatilidad en las reservas del BCV y presión sobre el tipo de cambio oficial reportada hoy."

            # B. Conexión segura a OpenRouter (Modelo LLaMA 3.1 Gratuito)
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=st.secrets["OPENROUTER_API_KEY"],
            )
            
            prompt_sistema = f"""
            Eres el "Asesor Maza Zavala", exdirector del BCV. Evalúa la política monetaria.
            Usa estas NOTICIAS ECONÓMICAS VENEZOLANAS DE HOY extraídas de internet:
            {contexto_web}
            
            IMPORTANTE Y OBLIGATORIO: Tu respuesta debe ser ÚNICAMENTE un formato JSON válido. No escribas nada antes ni después de las llaves {{}}.
            El JSON debe tener estas claves exactas:
            "bcv_rate" (ej. "Bs. 36.50"), "reserves" (ej. "$9.8 Billones"), "merey_price" (ej. "$65/bbl"), 
            "evaluacion" (tu crítica técnica escrita en primera persona), "auditoria_sudeban" (cumplimiento), 
            "shock_titulo" (título de evento imprevisto), "shock_desc" (descripción).
            """
            
            prompt_usuario = f"Propuesta: Cambio {tipo_cambio} Bs/USD | Intervención ${intervencion}M | Encaje {encaje}% | Tasa {tasa}% | FOGADE {fogade}. Justificación: {justificacion}"
            
            # Llamada al modelo
            response = client.chat.completions.create(
                model="google/gemini-2.0-flash-exp:free",
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": prompt_usuario}
                ],
                temperature=0.3
            )
            
            # Limpieza del formato JSON por si el modelo incluye etiquetas markdown
            respuesta_texto = response.choices[0].message.content.strip()
            if respuesta_texto.startswith("```json"):
                respuesta_texto = respuesta_texto.replace("```json", "", 1).replace("```", "")
            
            # Parsear datos
            datos = json.loads(respuesta_texto.strip())
            
            # C. Generación de Voz
            texto_a_hablar = f"Señores del Directorio, les habla el doctor Domingo Maza Zavala. {datos.get('evaluacion', '')}"
            tts = gTTS(text=texto_a_hablar, lang='es', slow=False)

            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)

            # D. Renderizado Visual
            st.audio(audio_fp, format='audio/mp3')
            st.caption("🔊 Escuchar dictamen del Dr. Maza Zavala")

            col1, col2, col3 = st.columns(3)
            col1.metric("Tasa BCV (Búsqueda Libre Hoy)", datos.get("bcv_rate", "N/A"))
            col2.metric("Reservas Internacionales", datos.get("reserves", "N/A"))
            col3.metric("Crudo Merey (Hoy)", datos.get("merey_price", "N/A"))
            
            st.markdown(f"""
            <div class="metric-box">
                <h3 style="margin-top:0;">Dictamen del Dr. Maza Zavala</h3>
                <p style="font-size: 1.1rem; line-height: 1.6;"><em>"{datos.get('evaluacion', '')}"</em></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-box" style="border-left-color: #10b981;">
                <h4 style="margin-top:0; color: #10b981;">Auditoría Regulatoria (SUDEBAN/FOGADE)</h4>
                <p>{datos.get('auditoria_sudeban', '')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="alert-box">
                <h3 style="margin-top:0; color: #ef4444;">🚨 CHOQUE MACROECONÓMICO INMINENTE</h3>
                <strong>{datos.get('shock_titulo', '')}</strong>
                <p>{datos.get('shock_desc', '')}</p>
                <p style="font-family: monospace; color: #fca5a5; margin-bottom:0;">"Señores directores, la coyuntura se ha complicado. Tienen 5 minutos para ajustar su decisión."</p>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error procesando la solicitud: Verifica tu conexión o formato. Detalle: {e}")
