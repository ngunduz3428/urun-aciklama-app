
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Ürün Açıklama Otomatı", layout="centered")

st.title("☕ Ürün Açıklama Otomatı")
st.write("Excel dosyanı yükle, biz senin için <strong>HTML formatında</strong> SEO dostu ürün açıklaması oluşturalım!", unsafe_allow_html=True)

# Ürün kategorisini algılayan fonksiyon
def detect_category(product_name: str) -> str:
    name = product_name.lower()
    if "kahve" in name:
        return "kahve_makinesi"
    elif "lazer" in name or "ipl" in name:
        return "ipl_lazer"
    elif "ütü" in name:
        return "utu"
    else:
        return "genel"

# Açıklama oluşturan fonksiyon
def generate_description(row):
    name = row.get("name [tr]", "")
    category = detect_category(name)
    html = f"<strong>{name}</strong> "

    if category == "kahve_makinesi":
        html += "ile geleneksel Türk kahvesini modern teknolojiyle buluşturun. "
    elif category == "ipl_lazer":
        html += "ile pürüzsüz bir cilt deneyimini evinizde yaşayın. "
    elif category == "utu":
        html += "ile kıyafetlerinizi zahmetsizce ütüleyin. "
    else:
        html += "ile fonksiyonel kullanım kolaylığını bir arada sunar. "

    def ekle(label, kolon):
        deger = str(row.get(kolon, "")).strip()
        if deger and deger.lower() != "nan":
            return f"<span><strong>{label}:</strong> {deger}</span>. "
        return ""

    html += ekle("Güç", "Güç")
    html += ekle("Bardak Kapasitesi", "Bardak kapasitesi")
    html += ekle("Su Kapasitesi", "Su tankı kapasitesi")
    html += ekle("Renk", "Ürün rengi")
    html += ekle("Sesli Uyarı", "Sesli uyarı")
    html += ekle("Otomatik Kapanma", "Otomatik kapanma")
    html += ekle("Emniyet Kilidi", "Emniyet klidi")
    html += ekle("Uyarı Işığı", "Uyarı ışığı")

    html += "<em>Detaylı ve güvenli kullanım için ideal bir tercihtir.</em>"
    return html

uploaded_file = st.file_uploader("Excel dosyanızı yükleyin", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    if "name [tr]" not in df.columns:
        st.error("Yüklediğiniz Excel dosyasında 'name [tr]' sütunu bulunamadı.")
    else:
        df["Ürün Açıklaması (HTML-SEO)"] = df.apply(generate_description, axis=1)
        st.dataframe(df[["name [tr]", "Ürün Açıklaması (HTML-SEO)"]])

        # Excel çıktısı olarak indir
        def convert_df(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name="Açıklamalar")
            return output.getvalue()

        excel_data = convert_df(df)
        st.download_button(
            label="📥 Excel Olarak İndir",
            data=excel_data,
            file_name="urun_aciklama_output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
