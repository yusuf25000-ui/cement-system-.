import streamlit as st
import pandas as pd
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="مكتب أبو محمد للتخليص", layout="wide")

# رابط الجدول (للقراءة فقط لضمان عدم حدوث أخطاء برمجية)
# هذا الرابط سيعمل دائماً لعرض التقارير
SHEET_ID = "1D5mzjR7lFqs6t4C8V0dWVdFki7bEXKubcTVchJe5ohM"
csv_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🏗️ نظام مكتب أبو محمد للتخليص</h1>", unsafe_allow_html=True)
st.divider()

tab1, tab2 = st.tabs(["📄 إصدار فاتورة جديدة", "📊 تقرير الحسابات"])

with tab1:
    st.subheader("📝 إدخال بيانات المعاملة")
    with st.form("invoice_form"):
        col1, col2 = st.columns(2)
        with col1:
            importer = st.text_input("اسم المستورد")
            driver = st.text_input("اسم السائق")
            plate = st.text_input("رقم اللوحة")
        with col2:
            bags = st.number_input("عدد الأكياس", min_value=0, step=1)
            fees = st.number_input("الرسوم (ريال)", min_value=0.0)
            date_val = st.date_input("التاريخ", datetime.now())
        
        submit = st.form_submit_button("✨ توليد الفاتورة للطباعة")

    if submit:
        if importer and driver:
            # تصميم فاتورة فخم واحترافي
            st.markdown(f"""
            <div style="direction: rtl; border: 5px solid #1E3A8A; padding: 30px; border-radius: 20px; background-color: white; color: black; font-family: 'Arial'; shadow: 10px 10px 5px grey;">
                <h2 style="text-align: center; color: #1E3A8A; margin-bottom: 0;">مكتب أبو محمد للتخليص الجمركي</h2>
                <p style="text-align: center; font-size: 14px; margin-top: 5px;">ثقة - سرعة - إنجاز</p>
                <hr style="border: 2px solid #1E3A8A;">
                <div style="display: flex; justify-content: space-between; font-size: 18px;">
                    <p><b>التاريخ:</b> {date_val}</p>
                    <p><b>رقم القاطرة:</b> {plate}</p>
                </div>
                <table style="width: 100%; font-size: 20px; border-collapse: collapse; margin-top: 20px;">
                    <tr style="background-color: #f8f9fa;"><td style="padding: 15px; border: 1px solid #ddd;"><b>المستورد:</b></td><td style="padding: 15px; border: 1px solid #ddd;">{importer}</td></tr>
                    <tr><td style="padding: 15px; border: 1px solid #ddd;"><b>السائق:</b></td><td style="padding: 15px; border: 1px solid #ddd;">{driver}</td></tr>
                    <tr style="background-color: #f8f9fa;"><td style="padding: 15px; border: 1px solid #ddd;"><b>الكمية:</b></td><td style="padding: 15px; border: 1px solid #ddd;">{bags:,} كيس</td></tr>
                </table>
                <div style="margin-top: 30px; padding: 20px; background-color: #E0E7FF; border-radius: 15px; text-align: center;">
                    <h2 style="margin: 0; color: #1E3A8A;">إجمالي الرسوم: {fees:,.2f} ريال</h2>
                </div>
                <p style="text-align: center; margin-top: 30px; font-size: 12px; color: #777;">صادر عن النظام الإلكتروني لمكتب أبو محمد</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.success("✅ الفاتورة جاهزة. خذ لقطة شاشة الآن.")
            
            # سطر البيانات المنظم للنسخ
            st.info("💡 لترتيب التقرير، انسخ السطر التالي وضعه في ملف جوجل شيت الخاص بك:")
            row_data = f"{date_val}, {importer}, {driver}, {plate}, {bags}, {fees}"
            st.code(row_data, language="text")
        else:
            st.error("يرجى إكمال البيانات")

with tab2:
    st.subheader("📊 تقرير القواطر والأكياس والمبالغ")
    if st.button("🔄 تحديث البيانات من جوجل"):
        try:
            df = pd.read_csv(csv_url)
            if not df.empty:
                # التأكد من تحويل الأعمدة لأرقام للحساب
                # العمود 4 هو الأكياس والعمود 5 هو الرسوم
                total_bags = pd.to_numeric(df.iloc[:, 4], errors='coerce').sum()
                total_money = pd.to_numeric(df.iloc[:, 5], errors='coerce').sum()
                
                c1, c2, c3 = st.columns(3)
                c1.metric("إجمالي القواطر", len(df))
                c2.metric("إجمالي الأكياس", f"{total_bags:,.0f}")
                c3.metric("إجمالي المبالغ", f"{total_money:,.2f} ريال")
                
                st.divider()
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("الجدول فارغ.")
        except:
            st.error("خطأ في جلب البيانات. تأكد من إدخال بيانات في الجدول أولاً.")
