import streamlit as st

st.title ("こんにちは、吉村ゼミ")

name = st.text_input("好きな言葉を入力してください")

st.write(name)

st.checkbox("同意します")
address = st.selectbox("次の中から現住所を教えてください",["京都府","大阪"])
st.write(address)

st.multiselect("次の中から複数選択してください",["映画","音楽","散歩"])
st.write(hobby)
camera_phote = st.camera_input("写真を撮影します")
if camera:
    st.image(camera, caption="写真", use_column_width=true)
