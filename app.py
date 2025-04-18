
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Ürün Açıklama Otomatı", layout="centered")

st.title("☕ Ürün Açıklama Otomatı")
st.write("Excel dosyanı yükle, biz senin için <strong>okuyucunun dikkatini çeken</strong> e-ticaret uyumlu ürün açıklamaları oluşturalım!", unsafe_allow_html=True)

def generate_marketing_description(row):
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
        body.append(f"{name} {power + ' gücüyle' if power else ''} kısa sürede lezzetli kahveler hazırlamanıza yardımcı olur.")

    if cups:
        body.append(f"{cups} fincan kapasitesi sayesinde kalabalık sofralar için idealdir.")

    if auto_off or sound_alert:
        safety = []
        if auto_off: safety.append(auto_off)
        if sound_alert: safety.append(sound_alert)
        body.append(f"{' ve '.join(safety).capitalize()}, güvenli ve zahmetsiz kullanım sunar.")

    if color:
        body.append(f"{color} rengi ve modern tasarımıyla mutfağınıza şıklık katar.")

    if lock or light:
        control = []
        if lock: control.append(lock)
        if light: control.append(light)
        body.append(f"{' ve '.join(control).capitalize()} ile kullanımda ekstra kontrol sağlar.")

    if not body:
        return ""

    return "\n\n".join(body)

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
        df["Ürün Açıklaması (Pazarlama Dili)"] = df.apply(generate_marketing_description, axis=1)

    st.success("✅ Açıklamalar oluşturuldu!")
    st.markdown("📋 Aşağıda oluşturulan açıklamaları inceleyebilirsin:")

    st.dataframe(df[["name [tr]", "Ürün Açıklaması (Pazarlama Dili)"]])

    excel_data = to_excel(df)
    st.download_button(
        label="📥 Açıklamaları Excel'e Aktar",
        data=excel_data,
        file_name="urun_aciklama_pazarlama.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
