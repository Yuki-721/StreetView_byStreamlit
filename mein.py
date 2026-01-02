import streamlit as st
from Picture_data import MAP_DATA
from streamlit_pannellum import streamlit_pannellum as pannellum
import base64
import os

# --- 1. 画像処理関数 ---
def get_base64_from_file(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "rb") as f:
        data = f.read()
        b64_str = base64.b64encode(data).decode()
        return f"data:image/jpeg;base64,{b64_str}"

#画面のデザイン
st.set_page_config(layout="wide") # 画面を広く使う設定に変更
st.title("🚶‍♂️ 簡易ストリートビュー")

# --- セッションステート管理 ---
if 'current_location' not in st.session_state:
    st.session_state['current_location'] = 'point1-1'

if 'button_log' not in st.session_state:
    st.session_state['button_log'] = False    

current_id = st.session_state['current_location']
current_data = MAP_DATA[current_id]

view_yaw = 0
base_yaw = current_data.get('start_yaw', 0)
if st.session_state['button_log'] == "⬇️":
    view_yaw = (base_yaw + 180)
else:
    view_yaw = base_yaw

# 画像読み込み
img_path = current_data['image_file']
img_url = get_base64_from_file(img_path)

# テスト用画像フォールバック
if img_url is None:
    if current_id == 'point_a':
        img_url = "https://pannellum.org/images/alma.jpg"
    else:
        img_url = "https://pannellum.org/images/cerro-armazon.jpg"

myconfig = {
    "panorama": img_url,
    "autoLoad": True,
    "autoRotate": False,
    "compass": True,
    "showZoomCtrl": False,
    "sceneFadeDuration": 1000,
    "yaw": view_yaw ,
}

# 比率 3:1 で分割（左を広く、右を狭く）
col_view, col_control = st.columns([3, 1]) 

# --- 左側：ビューワー ---
with col_view:
    pannellum(myconfig)

# --- 右側：操作パネル ---
st.write("---") # 区切り線
st.caption("移動する:")

 # ボタンを縦に並べて配置
 # use_container_width=True でボタンを横幅いっぱいに広げる
for target_id, button_label in current_data['connections'].items():
    if st.button(button_label, key=target_id,use_container_width=True):
        st.session_state['current_location'] = target_id
        st.session_state['button_log'] = button_label        
        st.rerun()