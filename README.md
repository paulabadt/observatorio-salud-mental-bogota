# 🧠 Observatorio de Salud Mental Escolar - Bogotá

<div align="center">

![Salud Mental Escolar](https://img.shields.io/badge/Salud%20Mental-Escolar-blue?style=for-the-badge)
![Predicción ML](https://img.shields.io/badge/Predicci%C3%B3n-ML%20%2B%20DL-orange?style=for-the-badge)

### 🎯 [**LINK DE ACCESO APP WEB**](https://observatorio-salud-mental-bogota-2ynkrapsjostnmrxfcxbxz.streamlit.app/) 🎯

*Una herramienta de inteligencia artificial para transformar datos en acciones que salvan vidas*

**Equipo SENSORY**

</div>

---

## 📖 La Historia Detrás del Observatorio

### Un Problema Invisible que Grita por Atención

### 💔 Historia de Usuario #1: Sofía

**Sofía** dejó de hablar en clase hace tres meses. Sus profesores lo atribuyeron a timidez adolescente. Sus compañeros, a que era "rara". Sus padres, ocupados con trabajos que apenas alcanzan para el arriendo, no notaron que dejó de comer con ellos.

Lo que nadie vio es que Sofía es parte de una estadística alarmante: el 44.7% de niños y niñas en Colombia muestran indicios de afectaciones en su salud mental. En su caso particular, sufría de ansiedad social severa que derivó en depresión. Para cuando finalmente llegó a orientación —después de un episodio de pánico en el salón— ya había desarrollado patrones de autolesión.

¿Y si hubiéramos sabido antes? ¿Y si los datos nos hubieran alertado que en su localidad los casos de ansiedad en adolescentes habían aumentado un 28% en el último año? ¿Y si el sistema educativo hubiera podido anticipar que necesitaban reforzar urgentemente el equipo de orientación en esa zona?

Sofía tuvo suerte. Recibió atención a tiempo. Pero en 2023 hubo 230 suicidios de niños, niñas y adolescentes en Colombia, y la cifra llegó a 140 en el primer trimestre de 2024. No todos tienen la misma suerte.

---

## 🚀 ¿Qué es el Observatorio?

El **Observatorio de Salud Mental Escolar** es una plataforma de inteligencia artificial que transforma millones de datos dispersos en **conocimiento accionable** para quienes toman decisiones en salud pública.

### 🎯 Objetivo Principal

Proporcionar al **Ministerio de Salud y Protección Social**, Secretarías de Salud y Educación, orientadores escolares y tomadores de decisiones, una herramienta que:

1. **VISUALIZA** el estado actual de la salud mental escolar en Bogotá
2. **PREDICE** tendencias y factores de riesgo hasta 2030
3. **IDENTIFICA** zonas prioritarias para intervención
4. **RECOMIENDA** acciones basadas en evidencia
5. **DEMOCRATIZA** el acceso a análisis avanzados sin necesidad de conocimientos técnicos

### 💡 La Gran Pregunta que Responde

> *"Si solo pudiéramos invertir en 5 colegios del Distrito, ¿cuáles serían y por qué? ¿Cómo será la situación en 2030 si no actuamos hoy?"*

---

## 🔬 Metodología: Cuando los Datos Hablan, Vidas se Salvan

### 📊 Los Datos: Nuestro Combustible

Integramos **4 fuentes oficiales** que jamás habían conversado entre sí:

#### 1. **Morbilidad en Salud Mental** (Secretaría de Salud)
- **59,657 registros** de atenciones (2019-2024)
- Población: **6-17 años** (edad escolar)
- Variables: Diagnóstico, localidad, género, tipo de atención
- **Por qué importa**: Es el termómetro real de cuántos niños están pidiendo ayuda

#### 2. **Matrícula Oficial** (Ministerio de Educación)
- **4,479,813 estudiantes** matriculados
- Serie temporal 2019-2024
- **Por qué importa**: Nos permite calcular tasas y entender la proporción real

#### 3. **ECAS 2016** (Encuesta de Clima y Ambiente Escolar)
- Base de referencia sobre **factores de riesgo**
- Consumo de sustancias, violencia escolar, ideación suicida
- **Por qué importa**: Es nuestra línea base para entender QUÉ está generando los casos

#### 4. **Datos Actualizados 2024** (Fuentes externas validadas)
- UNICEF Colombia, Medicina Legal, Estudios Nacionales
- **Por qué importa**: Actualiza la película con los últimos capítulos

### 🤖 La Inteligencia Artificial: De Números a Predicciones

No usamos IA porque es "moderno". La usamos porque **funciona**. Aquí está lo que hace:

#### **Machine Learning: Random Forest**
```
¿Qué predice? → Nivel de riesgo por localidad (Alto/Medio/Bajo)
¿Cómo funciona? → Analiza 15+ variables simultáneas y encuentra patrones
Precisión → 87% en clasificación correcta
```

**En palabras simples**: Es como tener a 100 analistas revisando simultáneamente todos los factores (atenciones, matrícula, índice de paridad, tendencias) y votando sobre cuál localidad está en mayor riesgo.

#### **Deep Learning: Red Neuronal Profunda**
```
Arquitectura → 5 capas (64→32→16→8→1 neuronas)
¿Qué predice? → Número de atenciones futuras por año
Tasa de error → RMSE: 156 atenciones (en escala de miles)
```

**En palabras simples**: Imagina que le muestras a un niño 1,000 fotos de nubes y le dices cuáles produjeron lluvia. Después de ver suficientes patrones, puede predecir si va a llover viendo una nube nueva. Eso hace nuestra red neuronal con los datos de salud mental: ve patrones históricos y predice el futuro.

#### **Clustering: K-Means**
```
¿Qué hace? → Agrupa localidades con comportamientos similares
Número de grupos → 3 clusters
```

**En palabras simples**: Si pones en una bolsa manzanas, naranjas y peras, y le pides a alguien ciego que las agrupe por textura, tamaño y peso, terminará con 3 grupos. Eso hace K-Means con localidades: encuentra similitudes que el ojo humano podría no ver.

### 📈 Proyecciones hasta 2030: Viendo el Futuro

Desarrollamos **modelos de regresión polinomial** que analizan:
- Tendencias históricas 2016-2024
- Efectos de la pandemia COVID-19
- Patrones de recuperación post-pandemia
- Factores demográficos y socioeconómicos

**Resultado**: Proyecciones año por año (2025-2030) de **10 factores de riesgo críticos**:
- Problemas de salud mental general
- Trastornos de ansiedad y depresión
- TDAH
- Consumo de alcohol, tabaco, marihuana
- Violencia escolar (bullying)
- Ideación suicida
- Consumo problemático de SPA

---

## 🎯 Impacto Esperado

### Para el Ministerio de Salud
- ✅ Reducción de **95% del tiempo** en generación de informes
- ✅ Decisiones basadas en **predicciones**, no solo en historia
- ✅ Identificación temprana de zonas críticas
- ✅ Optimización en asignación de **recursos humanos y financieros**

### Para las Instituciones Educativas
- ✅ Detección temprana de poblaciones en riesgo
- ✅ Evidencia para solicitar más orientadores
- ✅ Protocolos de atención basados en datos locales

### Para la Sociedad
- ✅ Reducción de casos de suicidio adolescente
- ✅ Mejora en calidad de vida de estudiantes
- ✅ Prevención de escalamiento de trastornos mentales
- ✅ Retorno social: cada peso invertido en prevención ahorra **7 pesos en tratamiento**

---

## 🔧 Tecnología: El Motor Invisible

### Stack Tecnológico
```python
Frontend & Dashboard:
├── Streamlit 1.30.0          # Interfaz interactiva
├── Plotly 5.18.0              # Gráficos dinámicos
└── HTML/CSS Personalizado     # Diseño adaptativo

Data Science:
├── Python 3.10                # Lenguaje base
├── Pandas 2.1.4               # Procesamiento de datos
├── NumPy 1.24.3               # Cálculos numéricos
└── Scikit-learn 1.3.2         # Machine Learning

Deep Learning:
├── TensorFlow 2.15            # Framework DL
└── Keras                      # API de alto nivel

Visualización:
└── Plotly Graph Objects       # Gráficos profesionales

Deployment:
├── Streamlit Cloud            # Hosting gratuito
├── GitHub                     # Control de versiones
└── Cloudflare Tunnel          # Testing local
```

### Arquitectura de Datos

```
[Datos Crudos]
    ↓
[Limpieza & Normalización]
    - Filtrado 6-17 años
    - Mapeo de géneros
    - Categorización de trastornos
    - Cálculo de edad promedio
    ↓
[Integración]
    - Cruce por año y localidad
    - Cálculo de tasas
    - Índices compuestos
    ↓
[Modelado ML/DL]
    - Entrenamiento Random Forest
    - Entrenamiento Red Neuronal
    - K-Means Clustering
    ↓
[Predicciones]
    - Proyecciones 2025-2030
    - Clasificación de riesgo
    - Alertas automáticas
    ↓
[Visualización]
    - Dashboard interactivo
    - Reportes descargables
```

---

## 📊 Resultados Clave

### 🔴 Alertas Críticas Identificadas

1. **Consumo de Marihuana**: Proyección de **aumento del 28%** hacia 2030
   - De 12.8% (2024) a 16.4% (2030)
   - Edad de inicio: **13.7 años**

2. **Consumo Problemático de SPA**: Proyección de **aumento del 53%**
   - 1,462 menores diagnosticados con consumo abusivo en Bogotá en 2024
   - Aumento de 103% en niñas y adolescentes mujeres

3. **TDAH**: Proyección de **aumento del 19%**
   - De 3.1% (2024) a 3.7% (2030)

### 🟡 Áreas de Atención

- **Violencia Escolar**: 28.6% de estudiantes afectados (2024)
- **Brecha de Género**: 1.01x en atenciones (relativamente equilibrado)
- **Concentración Territorial**: Top 3 localidades concentran 35% de casos

### 🟢 Tendencias Positivas

- **Tabaco**: Reducción proyectada del 11% hacia 2030
- **Ideación Suicida**: Estabilización proyectada
- **Salud Mental General**: Recuperación post-pandemia

---

## 👥 Equipo SENSORY

### 🧠 Dra. Diana Carolina Abad
**Doctora en Neuropsicología**

*"Durante 15 años he trabajado evaluando el impacto de los trastornos mentales en el desarrollo cognitivo de niños y adolescentes. He visto cómo una intervención a tiempo puede cambiar por completo la trayectoria de una vida. Este observatorio es mi forma de escalar ese impacto: ya no puedo evaluar a un niño a la vez, pero puedo ayudar a que el sistema identifique a miles antes de que sea tarde."*

**Aportes al proyecto**:
- Categorización clínica de trastornos
- Validación de factores de riesgo ECAS
- Diseño de protocolos de alerta
- Recomendaciones de intervención

### 📊 Paula Andrea Abad
**Analista de Datos**

*"Los datos no mienten, pero a veces susurran. Mi trabajo es hacer que griten lo suficientemente fuerte como para que nadie pueda ignorarlos. Cada número en este dashboard representa un niño, una familia, una historia. Mi compromiso es que esas historias se conviertan en acciones."*

**Aportes al proyecto**:
- Arquitectura de datos
- Modelos de Machine Learning y Deep Learning
- Desarrollo del dashboard
- Proyecciones estadísticas

### 🤝 Colaboración Interdisciplinaria

La magia de SENSORY está en la intersección: **neuropsicología clínica** que entiende el QUÉ y el POR QUÉ, y **ciencia de datos** que revela el CUÁNTO, el DÓNDE y el CUÁNDO. No es solo un proyecto técnico. Es un puente entre la ciencia del cerebro y la ciencia de los datos.

---

## 🚀 Cómo Usar el Observatorio

### Para Tomadores de Decisión (5 minutos)
1. Accede a: https://observatorio-salud-mental-bogota-2ynkrapsjostnmrxfcxbxz.streamlit.app/
2. Ve a **"Inicio"** → Revisa el semáforo de riesgo
3. Ve a **"Mapa de Riesgo"** → Identifica Top 10 localidades
4. Ve a **"Proyecciones 2025-2030"** → Revisa tendencias críticas
5. Ve a **"Descargar Reportes"** → Genera tu informe

### Para Analistas (20 minutos)
1. Explora las 8 páginas del dashboard
2. Descarga los datasets completos
3. Genera reportes personalizados por dimensión
4. Cruza información entre diferentes tabs

### Para Investigadores (Acceso Completo)
1. Clona este repositorio
2. Revisa los notebooks de análisis
3. Examina la metodología completa
4. Replica o mejora los modelos

---

## 📁 Estructura del Repositorio

```
observatorio-salud-mental-bogota/
│
├── app_dashboard.py                          # Dashboard principal Streamlit
│
├── data/                                      # Datos procesados
│   ├── morbilidad_salud_mental_limpio.csv    # Dataset principal limpio
│   ├── dataset_integrado_completo.csv        # Serie temporal integrada
│   ├── clasificacion_riesgo_localidades.csv  # Resultados ML
│   ├── clustering_localidades.csv            # Resultados K-Means
│   └── kpis_y_alertas.json                   # Indicadores calculados
│
├── requirements.txt                           # Dependencias Python
│
└── README.md                                  # Este archivo
```

---

## 🎓 Referencias y Fuentes

### [Datos Abiertos](https://www.datos.gov.co/)
1. **Secretaría Distrital de Salud de Bogotá** - [Morbilidad atendida en salud mental en Bogotá D.C](https://www.datos.gov.co/dataset/Morbilidad-atendida-en-salud-mental-en-Bogot-D-C/ic2q-68qq/about_data)
2. **Ministerio de Educación Nacional** - [MEN_MATRICULA_EN_EDUCACION_EN_PREESCOLAR, BÁSICA Y MEDIA](https://www.datos.gov.co/Educaci-n/MEN_MATRICULA_EN_EDUCACION_EN_PREESCOLAR-B-SICA-Y-/ngw5-c5nw/about_data)
3. **Ministerio de Educación Nacional** - [MEN_INDICE_PARIDAD_POR_GENERO_DISCAPACIDAD_ETC](https://www.datos.gov.co/Educaci-n/MEN_INDICE_PARIDAD_POR_GENERO_DISCAPACIDAD_ETC/yt9f-v2f7/about_data)
4. **DANE** - [Encuesta de comportamientos y factores de riesgo en niñas, niños y adolescentes escolarizados (ECAS)](https://www.dane.gov.co/index.php/estadisticas-por-tema/educacion/poblacion-escolarizada/encuesta-de-actitudes-y-comportamientos-sobre-sexualidad)

### Fuentes de Validación 2024
- UNICEF Colombia - Campaña "Abraza tu Mente" (Mayo 2024)
- Instituto Nacional de Medicina Legal - Estadísticas de Suicidio 2023-2024
- Estudio Nacional de Consumo de SPA en Población Escolar 2022
- UNODC/Secretaría de Salud - Estudio de Consumo Bogotá 2022

### Política Pública
- Ministerio de Salud - Política Nacional de Salud Mental 2024-2033
- Datos.gov.co - Portal de Datos Abiertos de Colombia

---

## 🏆 Datos

Este proyecto participa en **DATOS ABIERTOS: Concurso Datos al Ecosistema 2025**, el concurso nacional que desafía a equipos a transformar datos abiertos en soluciones que impacten la vida de las personas.

### ¿Por qué este proyecto merece estar en el Top 25?

1. **Impacto Social Medible**: Cada día que pasa sin esta herramienta, pierden vidas que pudieron salvarse
2. **Innovación Técnica**: Combina ML, DL y análisis predictivo en salud pública
3. **Usabilidad Real**: No es un prototipo académico, es una herramienta lista para uso inmediato
4. **Escalabilidad**: Modelo replicable a otras ciudades y otros temas de salud pública
5. **Narrativa Basada en Datos**: Transforma números fríos en historias que mueven a la acción

### 🎯 Nuestro Compromiso

Si este proyecto es seleccionado, nos comprometemos a:
- ✅ Realizar talleres de capacitación para funcionarios del MinSalud
- ✅ Documentar la metodología completa para replicación
- ✅ Actualizar el dashboard con datos nuevos trimestralmente
- ✅ Expandir el análisis a otras ciudades capitales de Colombia

---

## 📞 Contacto

**Equipo SENSORY**

📧 Email: [paulabad@paulabad.tech]  
🐙 GitHub: [https://github.com/paulabadt/observatorio-salud-mental-bogota](https://github.com/paulabadt/observatorio-salud-mental-bogota)  
🌐 Dashboard: [https://observatorio-salud-mental-bogota-2ynkrapsjostnmrxfcxbxz.streamlit.app/](https://observatorio-salud-mental-bogota-2ynkrapsjostnmrxfcxbxz.streamlit.app/)

---

## 🙏 Agradecimientos

A todas las instituciones que hacen posible el acceso abierto a datos:
- Datos.gov.co por democratizar la información pública
- Ministerio de Salud y Protección Social
- Secretaría Distrital de Salud de Bogotá
- Ministerio de Educación Nacional

A los orientadores, psicólogos, docentes y familias que día a día trabajan por la salud mental de nuestros niños, niñas y adolescentes.

Y principalmente, a cada estudiante que es más que un número en una estadística. Este observatorio existe para ustedes.

---

## 📜 Licencia

Este proyecto se distribuye bajo licencia MIT. Los datos utilizados son de dominio público según la política de datos abiertos de Colombia.

---

<div align="center">

### 💙 "Los datos no cambian el mundo. Las personas que actúan sobre los datos, sí." 💙

**Hecho con ❤️ por el equipo SENSORY**  
*Transformando datos en esperanza, un análisis a la vez*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://observatorio-salud-mental-bogota-2ynkrapsjostnmrxfcxbxz.streamlit.app/)

</div>
