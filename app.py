
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Ürün Açıklama Otomatı", layout="centered")

st.title("☕ Ürün Açıklama Otomatı")
st.write("Excel dosyanı yükle, biz senin için ürün açıklaması oluşturalım!")

def generate_description_safe(row):
    name = str(row.get("name [tr]", ""))
    power = str(row.get("Güç", "")).strip()
    auto_off = "otomatik kapanma özelliği" if "Evet" in str(row.get("Otomatik kapanma", "")) else ""
    sound_alert = "sesli uyarı sistemi" if "Evet" in str(row.get("Sesli uyarı", "")) else ""
    tank = str(row.get("Su tankı kapasitesi", "")).split("-")[-1] if pd.notna(row.get("Su tankı kapasitesi")) else ""
    cups = str(row.get("Bardak kapasitesi", "")).split("_")[-1] if pd.notna(row.get("Bardak kapasitesi")) else ""
    color = str(row.get("Ürün rengi", "")).split("-")[-1] if pd.notna(row.get("Ürün rengi")) else ""
    lock = "emniyet kilidi" if "Var" in str(row.get("Emniyet klidi", "")) else ""
    light = "uyarı ışığı" if "Var" in str(row.get("Uyarı ışığı", "")) else ""

    features = [power + " gücü" if power else "", auto_off, sound_alert,
                f"{tank} L su tankı" if tank else "", f"{cups} bardak kapasitesi" if cups else "",
                f"{color} tasarımı" if color else "", lock, light]
    features = [f for f in features if f]

    description = f"{name}, " + ", ".join(features) + " ile donatılmıştır. Hem şık tasarımıyla hem de kullanım kolaylığıyla öne çıkar."
    return description

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
        df["Ürün Açıklaması"] = df.apply(generate_description_safe, axis=1)

    st.success("✅ Açıklamalar oluşturuldu!")

    st.dataframe(df)

    excel_data = to_excel(df)
    st.download_button(
        label="📥 Excel'e Aktar",
        data=excel_data,
        file_name="urun_aciklama_sonuclari.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
