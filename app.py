
import streamlit as st
import pandas as pd
from io import BytesIO
import random

st.set_page_config(page_title="Ürün Açıklama Otomatı", layout="centered")
st.title("☕ Ürün Açıklama Otomatı")
st.write("Excel dosyanı yükle, <strong>ürüne uygun</strong>, <strong>HTML formatında</strong> ve <strong>SEO dostu</strong> açıklamalar oluşturalım!", unsafe_allow_html=True)

def generate_unique_description(row):
    def clean(value):
        return str(value).strip() if pd.notna(value) and str(value).strip().lower() != "nan" else ""

    name = clean(row.get("name [tr]"))
    power = clean(row.get("Güç"))
    auto_off = "otomatik kapanma özelliği" if "Evet" in clean(row.get("Otomatik kapanma")) else ""
    sound_alert = "sesli uyarı sistemi" if "Evet" in clean(row.get("Sesli uyarı")) else ""
    tank = clean(row.get("Su tankı kapasitesi")).split("-")[-1]
    cups = clean(row.get("Bardak kapasitesi")).split("_")[-1]
    color = clean(row.get("Ürün rengi")).split("-")[-1]
    lock = "emniyet kilidi" if "Var" in clean(row.get("Emniyet klidi")) else ""
    light = "uyarı ışığı" if "Var" in clean(row.get("Uyarı ışığı")) else ""

    body = []

    if name:
        body.append(f"<strong>{name}</strong>")

    if power:
        body.append(f"<span>{power} gücü</span> ile kahvenizi ideal sıcaklıkta hazırlar")

    if cups:
        cups_text = random.choice([
            f"<span>{cups} fincan kapasitesi</span> ile ideal miktarda servis yapar",
            f"Tek seferde <span>{cups} fincan</span> kahve hazırlama imkanı sunar"
        ])
        body.append(cups_text)

    if auto_off or sound_alert:
        safety_features = []
        if auto_off: safety_features.append(auto_off)
        if sound_alert: safety_features.append(sound_alert)
        body.append(", ".join(safety_features).capitalize() + " ile güvenli kullanım sağlar")

    if color:
        body.append(f"<span>{color} tasarımı</span> mutfağınıza uyum sağlar")

    if lock or light:
        security_features = []
        if lock: security_features.append(lock)
        if light: security_features.append(light)
        body.append(", ".join(security_features).capitalize() + " ile kullanım kolaylığı sunar")

    # Açıklama cümlelerini çeşitlendirme
    if body:
        conclusion_options = [
            "Türk kahvesi keyfinizi pratik ve şık bir deneyime dönüştürür.",
            "Kahve hazırlamayı konforlu hale getirir.",
            "Geleneksel lezzeti modern teknolojiyle buluşturur."
        ]
        body.append(f"<em>{random.choice(conclusion_options)}</em>")

    return ". ".join(body) if body else ""

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
        df["Ürün Açıklaması (HTML-SEO)"] = df.apply(generate_unique_description, axis=1)

    st.success("✅ Açıklamalar oluşturuldu!")
    st.dataframe(df[["name [tr]", "Ürün Açıklaması (HTML-SEO)"]])

    excel_data = to_excel(df)
    st.download_button(
        label="📥 HTML Açıklamaları İndir",
        data=excel_data,
        file_name="urun_aciklama_html_seo.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
