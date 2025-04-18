
import streamlit as st
import pandas as pd
from io import BytesIO
import random

st.set_page_config(page_title="Ürün Açıklama Otomatı", layout="centered")
st.title("☕ Ürün Açıklama Otomatı")
st.write("Excel dosyanı yükle, <strong>yalnızca dolu alanlara göre</strong> <strong>SEO uyumlu</strong> ve <strong>HTML formatlı</strong> açıklamaları otomatik olarak oluştur!", unsafe_allow_html=True)

def generate_focused_html(row):
    def clean(val):
        return str(val).strip() if pd.notna(val) and str(val).strip().lower() != "nan" else ""

    name = clean(row.get("name [tr]"))
    power = clean(row.get("Güç"))
    auto_off = "otomatik kapanma özelliği" if "Evet" in clean(row.get("Otomatik kapanma")) else ""
    sound_alert = "sesli uyarı sistemi" if "Evet" in clean(row.get("Sesli uyarı")) else ""
    tank = clean(row.get("Su tankı kapasitesi")).split("-")[-1]
    cups = clean(row.get("Bardak kapasitesi")).split("_")[-1]
    color = clean(row.get("Ürün rengi")).split("-")[-1]
    lock = "emniyet kilidi" if "Var" in clean(row.get("Emniyet klidi")) else ""
    light = "uyarı ışığı" if "Var" in clean(row.get("Uyarı ışığı")) else ""

    parts = []

    if name:
        parts.append(f"<strong>{name}</strong>")

    if power:
        parts.append(f"<span>{power} gücü</span> ile ideal sıcaklıkta kahvenizi hazırlar")

    if cups:
        parts.append(f"<span>{cups} fincan kapasitesi</span> ile aynı anda servis kolaylığı sunar")

    safety = []
    if auto_off: safety.append(auto_off)
    if sound_alert: safety.append(sound_alert)
    if safety:
        parts.append(", ".join(safety).capitalize() + " ile güvenli ve rahat kullanım sağlar")

    if color:
        parts.append(f"<span>{color} tasarımı</span> mutfağınıza modern bir dokunuş katar")

    control = []
    if lock: control.append(lock)
    if light: control.append(light)
    if control:
        parts.append(", ".join(control).capitalize() + " ile kullanımda ekstra kontrol sağlar")

    if not parts:
        return ""

    conclusion = random.choice([
        "Türk kahvesi keyfini teknolojiyle buluşturan ideal bir seçimdir.",
        "Kahve deneyiminizi modernleştiren akıllı bir çözümdür.",
        "Geleneksel lezzeti fonksiyonel detaylarla sunar."
    ])

    html = ". ".join(parts) + f". <em>{conclusion}</em>"
    return html

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

uploaded_file = st.file_uploader("📂 Excel dosyasını yükle (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("Dosya yüklendi:")
    st.dataframe(df)

    with st.spinner("Açıklamalar yazılıyor..."):
        df["Ürün Açıklaması (HTML-SEO)"] = df.apply(generate_focused_html, axis=1)

    st.success("✅ Açıklamalar oluşturuldu!")
    st.dataframe(df[["name [tr]", "Ürün Açıklaması (HTML-SEO)"]])

    excel_data = to_excel(df)
    st.download_button(
        label="📥 HTML Açıklamaları İndir",
        data=excel_data,
        file_name="urun_aciklama_html_seo.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
