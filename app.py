from datetime import datetime
import pytz
import streamlit as st
import pandas as pd
# 顯示台灣時間
tz = pytz.timezone("Asia/Taipei")
now = datetime.now(tz)
st.write("📅 現在台灣時間：", now.strftime("%Y-%m-%d %H:%M:%S"))

st.set_page_config(page_title="SimpleReceiveApp 雲端版", layout="centered")

if "records" not in st.session_state:
    st.session_state.records = []

st.title("📦 SimpleReceiveApp（雲端版）")
st.write("記錄包裹收發、簽收時間、住戶資訊，自動產生流水號。")

with st.form("receive_form"):
    sn = len(st.session_state.records) % 500 + 1
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("📆 收貨日期", datetime.today())
        address = st.text_input("🏠 住戶地址")
        recipient = st.text_input("👤 收件人姓名")
        qty = st.number_input("📦 件數", min_value=1, step=1)
    with col2:
        company = st.text_input("🚚 貨運公司")
        location = st.text_input("📍 擺放位置")
        dispatcher = st.text_input("📮 收貨管理員")
        signer = st.text_input("✍️ 發貨管理員")
        signed = st.checkbox("✅ 已領取")

    sign_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if signed else ""
    submitted = st.form_submit_button("儲存紀錄")

    if submitted:
        if address and recipient and company and location:
            st.session_state.records.append({
                "流水號": sn,
                "收貨日期": str(date),
                "住址": address,
                "收件人": recipient,
                "件數": qty,
                "貨運公司": company,
                "擺放位置": location,
                "收貨管理員": dispatcher,
                "發貨管理員": signer,
                "已領取": "是" if signed else "否",
                "簽收時間": sign_time
            })
            st.success(f"第 {sn} 筆紀錄已儲存 ✅")
        else:
            st.warning("請填寫所有欄位")

st.markdown("---")
st.subheader("📋 所有收發記錄")
if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    st.dataframe(df, use_container_width=True)

    received_df = df[df["已領取"] == "是"]
    pending_df = df[df["已領取"] == "否"]

    with st.expander("✅ 已領取清單"):
        st.dataframe(received_df, use_container_width=True)
    with st.expander("📭 未領取清單"):
        st.dataframe(pending_df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📤 下載 CSV", data=csv, file_name="收發記錄.csv", mime="text/csv")
else:
    st.info("目前尚無紀錄。")
