import streamlit as st
from google import genai
from google.genai import types
import json
from gtts import gTTS
import io

# 1. Configuración de la página y Diseño Visual
st.set_page_config(page_title="Simulador BCV - Maza Zavala", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main { background-color: #0b101d; color: #ffffff; }
    h1, h2, h3 { color: #f59e0b !important; font-family: 'Courier New', Courier, monospace; }
    .stSlider > div > div > div { background-color: #f59e0b; }
    
    /* Forzado de color blanco puro en los recuadros */
    .metric-box { background-color: #0f172a; border: 1px solid #1e293b; padding: 15px; border-radius: 10px; border-left: 4px solid #f59e0b; margin-bottom: 15px; color: #ffffff !important;}
    .alert-box { background-color: #450a0a; border: 1px solid #7f1d1d; padding: 15px; border-radius: 10px; border-left: 4px solid #ef4444; margin-top: 20px; color: #ffffff !important;}
    
    /* Asegurar que todos los párrafos y negritas hereden el blanco */
    .metric-box p, .metric-box em, .metric-box strong, 
    .alert-box p, .alert-box em, .alert-box strong { color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

# 2. Encabezado
st.markdown("<h1>🏛️ Directorio Extraordinario del BCV</h1>", unsafe_allow_html=True)
st.markdown("### Asesor Artificial Maza Zavala")

# 3. Panel Lateral
with st.sidebar:
    st.header("Mesa Técnica")
    st.caption("Ajuste los parámetros para mitigar el Pass-Through (ERPT)")
    
    tipo_cambio = st.slider("1. Tipo de Cambio Objetivo (Bs/USD)", 25.0, 120.0, 45.5, step=0.1)
    intervencion = st.slider("2. Intervención Semanal (M$ USD)", 10, 300, 80, step=5)
    encaje = st.number_input("3. Encaje Legal (%)", min_value=10, max_value=100, value=73)
    tasa = st.number_input("4. Tasa de Interés (%)", min_value=5, max_value=200, value=40)
    
    fogade = st.selectbox("5. Cobertura FOGADE", [
        "Límite Oficial Vigente",
        "Garantía Aumentada",
        "Ajuste en Divisas"
    ])
    justificacion = st.text_area("6. Justificación Técnica", "Buscamos anclar las expectativas...")
    submit_btn = st.button("Someter Decreto a Maza Zavala", use_container_width=True)

# 4. Lógica de IA y Procesamiento Tolerante a Fallos
if submit_btn:
    with st.spinner("🔍 Analizando bases de datos del BCV y calculando dictamen..."):
        datos = {}
        try:
            # Intento de conexión con Google Gemini
            client = genai.Client(api_key=st.secrets.get("GEMINI_API_KEY", ""))
            
            system_instruction = """Eres el Dr. Maza Zavala. Evalúa la política monetaria en JSON estricto: {"bcv_rate", "reserves", "merey_price", "evaluacion", "auditoria_sudeban", "shock_titulo", "shock_desc"}."""
            prompt = f"Cambio: {tipo_cambio} | Intervención: {intervencion}M | Encaje: {encaje}% | Tasa: {tasa}%"
            
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.3,
                    response_mime_type="application/json",
                )
            )
            datos = json.loads(response.text)
            
        except Exception as e:
            # ==========================================
            # SISTEMA DE RESCATE (FALLBACK) - SE ACTIVA SI LA API FALLA
            # ==========================================
            st.toast("⚠️ Servidor saturado. Operando con el motor de análisis econométrico local.", icon="⚙️")
            
            # Generamos la evaluación dinámicamente según lo que escogió el estudiante
            eval_texto = f"He revisado la propuesta técnica. Fijar la tasa en {tipo_cambio} bolívares "
            if intervencion < 80:
                eval_texto += f"con una intervención débil de {intervencion} millones de dólares no frenará la devaluación. "
            else:
                eval_texto += f"respaldado por {intervencion} millones en intervención ayudará a contener el mercado. "
                
            if encaje > 60:
                eval_texto += f"Sin embargo, sostener un encaje del {encaje}% sigue asfixiando el crédito productivo bajo el modelo de Butler."
            else:
                eval_texto += f"El alivio del encaje al {encaje}% dinamiza la banca, pero inyectará liquidez peligrosa."

            datos = {
                "bcv_rate": "Bs. 582,6862",
                "reserves": "$12.404 MM",
                "merey_price": "$87,77/bbl",
                "evaluacion": eval_texto,
                "auditoria_sudeban": "Se requiere monitorear los índices de liquidez de la banca.",
                "shock_titulo": "Presión Inflacionaria Repentina",
                "shock_desc": "La liquidez excedentaria ha impactado el mercado paralelo. Ajusten la política en los próximos 10 minutos."
            }

        # 5. Generación de Voz y Renderizado Visual
        try:
            texto_a_hablar = f"Señores del Directorio, les habla el doctor Domingo Maza Zavala. {datos.get('evaluacion', '')}"
            tts = gTTS(text=texto_a_hablar, lang='es', slow=False)
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)
            
            st.audio(audio_fp, format='audio/mp3')
            st.caption("🔊 Escuchar dictamen del Dr. Maza Zavala")
        except Exception as audio_e:
            st.warning("El módulo de audio no pudo cargar, lea el dictamen en pantalla.")

        col1, col2, col3 = st.columns(3)
        col1.metric("Tasa Oficial BCV", datos.get("bcv_rate", "N/A"))
        col2.metric("Reservas Internacionales", datos.get("reserves", "N/A"))
        col3.metric("Crudo Merey (Referencial)", datos.get("merey_price", "N/A"))
        
        st.markdown(f"""
        <div class="metric-box">
            <h3 style="margin-top:0;">Dictamen del Dr. Maza Zavala</h3>
            <p style="font-size: 1.1rem; line-height: 1.6; color: #ffffff;"><em>"{datos.get('evaluacion', '')}"</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-box" style="border-left-color: #10b981;">
            <h4 style="margin-top:0; color: #10b981;">Auditoría Regulatoria (SUDEBAN)</h4>
            <p style="color: #ffffff;">{datos.get('auditoria_sudeban', '')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="alert-box">
            <h3 style="margin-top:0; color: #ef4444;">🚨 CHOQUE MACROECONÓMICO INMINENTE</h3>
            <strong style="color: #ffffff;">{datos.get('shock_titulo', '')}</strong>
            <p style="color: #ffffff;">{datos.get('shock_desc', '')}</p>
        </div>
        """, unsafe_allow_html=True)
