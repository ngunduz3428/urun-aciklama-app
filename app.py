
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Ürün Açıklama Otomatı", layout="centered")

st.title("☕ Ürün Açıklama Otomatı")
st.write("Excel dosyanı yükle, biz senin için <strong>HTML formatında</strong> SEO dostu ürün açıklaması oluşturalım!", unsafe_allow_html=True)

def generate_html_description(row):
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

    features = []
    if power: features.append(f"<span>{power} gücü</span>")
    if auto_off: features.append(f"<span>{auto_off}</span>")
    if sound_alert: features.append(f"<span>{sound_alert}</span>")
    if tank: features.append(f"<span>{tank} L su tankı</span>")
    if cups: features.append(f"<span>{cups} bardak kapasitesi</span>")
    if color: features.append(f"<span>{color} tasarımı</span>")
    if lock: features.append(f"<span>{lock}</span>")
    if light: features.append(f"<span>{light}</span>")

    if name:
        desc = f"<strong>{name}</strong>"
        if features:
            desc += ", " + ", ".join(features) + "."
        desc += " Bu <em>kahve makinesi</em>, <strong>şık tasarımı</strong> ve <strong>kullanım kolaylığı</strong> ile mutfağınızın vazgeçilmezi olacak."
    else:
        desc = ""

    return desc

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

    with st.spinner("HTML açıklamalar oluşturuluyor..."):
        df["Ürün Açıklaması (HTML)"] = df.apply(generate_html_description, axis=1)

    st.success("✅ Açıklamalar oluşturuldu!")
    st.markdown("📋 Aşağıda oluşturulan HTML açıklamaları yer almakta:")

    st.dataframe(df[["name [tr]", "Ürün Açıklaması (HTML)"]])

    excel_data = to_excel(df)
    st.download_button(
        label="📥 HTML Açıklamaları Excel'e Aktar",
        data=excel_data,
        file_name="urun_aciklama_html.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
