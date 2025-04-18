
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Ürün Açıklama Otomatı", layout="centered")

st.title("☕ Ürün Açıklama Otomatı")
st.write("Excel dosyanı yükle, biz senin için <strong>HTML formatında</strong>, <strong>SEO uyumlu</strong> ve <strong>pazarlama dilinde</strong> ürün açıklamaları oluşturalım!", unsafe_allow_html=True)

def generate_seo_html_description(row):
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

    parts = []

    if name:
        intro = f"<strong>{name}</strong>, "
    else:
        intro = ""

    if power:
        parts.append(f"<span>{power} gücüyle</span> kısa sürede kahve hazırlamanızı sağlar")

    if cups:
        parts.append(f"<span>{cups} fincan kapasitesi</span> ile kalabalık sofralara hitap eder")

    safety = []
    if auto_off: safety.append(auto_off)
    if sound_alert: safety.append(sound_alert)
    if safety:
        parts.append(f"{' ve '.join(safety).capitalize()}, <span>güvenli ve pratik kullanım</span> sunar")

    if color:
        parts.append(f"<span>{color} tasarımı</span> ile mutfağınıza estetik katar")

    control = []
    if lock: control.append(lock)
    if light: control.append(light)
    if control:
        parts.append(f"{' ve '.join(control).capitalize()} sayesinde <span>kullanım kolaylığı</span> sağlar")

    if not parts:
        return ""

    html = f"{intro}" + ". ".join(parts) + ". <em>Şık tasarımı ve fonksiyonel yapısıyla mutfağınızın vazgeçilmezi olmaya aday.</em>"

    return html

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

uploaded_file = st.file_uploader("📂 Excel dosyasını yükle (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("Dosya yüklendi! İçeriği aşağıda:")
    st.dataframe(df)

    with st.spinner("Açıklamalar oluşturuluyor..."):
        df["Ürün Açıklaması (HTML-SEO)"] = df.apply(generate_seo_html_description, axis=1)

    st.success("✅ Açıklamalar oluşturuldu!")
    st.markdown("📋 Aşağıda oluşturulan HTML açıklamaları yer almakta:")

    st.dataframe(df[["name [tr]", "Ürün Açıklaması (HTML-SEO)"]])

    excel_data = to_excel(df)
    st.download_button(
        label="📥 HTML Açıklamaları Excel'e Aktar",
        data=excel_data,
        file_name="urun_aciklama_html_seo.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
