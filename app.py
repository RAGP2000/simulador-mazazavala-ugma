import streamlit as st
from google import genai
from google.genai import types
import json
from gtts import gTTS
import io

# 1. Configuración de la página y Diseño Visual Premium (Inyección CSS)
st.set_page_config(page_title="Simulador BCV - Maza Zavala", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* Estilos para igualar el impacto visual del frontend web */
    .main { background-color: #0b101d; color: #f1f5f9; }
    h1, h2, h3 { color: #f59e0b !important; font-family: 'Courier New', Courier, monospace; }
    .stSlider > div > div > div { background-color: #f59e0b; }
    .metric-box { background-color: #0f172a; border: 1px solid #1e293b; padding: 15px; border-radius: 10px; border-left: 4px solid #f59e0b; margin-bottom: 15px;}
    .alert-box { background-color: #450a0a; border: 1px solid #7f1d1d; padding: 15px; border-radius: 10px; border-left: 4px solid #ef4444; margin-top: 20px;}
    </style>
""", unsafe_allow_html=True)

# 2. Encabezado de la Aplicación
st.markdown("<h1>🏛️ Directorio Extraordinario del BCV</h1>", unsafe_allow_html=True)
st.markdown("### Asesor Artificial Maza Zavala (Con Grounding en Tiempo Real)")

# 3. Panel Lateral: Captura de Datos de los Estudiantes (Actualizado y Protegido)
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
    
    # Envío directo. Las credenciales se manejan de forma segura en el backend
    submit_btn = st.button("Someter Decreto a Maza Zavala", use_container_width=True)

# 4. Lógica de IA y Procesamiento con Automatización de Credenciales
if submit_btn:
    with st.spinner("🔍 Analizando bases de datos del BCV y buscando indicadores económicos de hoy..."):
        try:
            # Conexión automatizada utilizando los Secrets del servidor en la nube
            client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
            
            system_instruction = """
            Eres el "Asesor Maza Zavala", exdirector del BCV. Evalúas planes del Directorio.
            Usa la herramienta Google Search obligatoriamente para buscar los datos reales de Venezuela HOY (Dólar oficial, reservas, precio crudo Merey).
            Aplica la lógica del ERPT asimétrico y la brecha del producto de Leo Butler (1996).
            Genera siempre un Shock Macroeconómico de Alerta al final.
            
            IMPORTANTE: Devuelve tu respuesta ÚNICAMENTE en un JSON válido con estas claves exactas:
            "bcv_rate", "reserves", "merey_price", "evaluacion", "auditoria_sudeban", "shock_titulo", "shock_desc".
            """
            
            prompt_estudiantes = f"""
            Propuesta:
            Tipo Cambio: {tipo_cambio} Bs/USD | Intervención: ${intervencion}M | Encaje: {encaje}% | Tasa: {tasa}% | FOGADE: {fogade}
            Justificación: {justificacion}
            """
            
            # Llamada utilizando la arquitectura vigente de última generación
            response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=prompt_estudiantes,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                    temperature=0.3,
                    response_mime_type="application/json",
                )
            )
            
            # Extraer y parsear la respuesta JSON de la IA
            datos = json.loads(response.text)
            
            # Generación del archivo de voz (Text-to-Speech) a partir del dictamen
            texto_a_hablar = f"Señores del Directorio, les habla el doctor Domingo Maza Zavala. {datos.get('evaluacion', '')}"
            tts = gTTS(text=texto_a_hablar, lang='es', slow=False)

            # Almacenamiento directo en el buffer de memoria
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)

            # 5. Renderizado Visual y Multimodal del Dictamen (Output)
            st.audio(audio_fp, format='audio/mp3')
            st.caption("🔊 Escuchar dictamen del Dr. Maza Zavala")

            col1, col2, col3 = st.columns(3)
            col1.metric("Tasa Oficial BCV (Grounding)", datos.get("bcv_rate", "N/A"))
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
            st.error(f"Fallo en los cálculos matriciales: {e}")
