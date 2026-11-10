"""실행: python -m streamlit run app.py"""
import sqlite3
import streamlit as st
from pathlib import Path
from avatar_api import STYLES, get_avatar
from resident_db import init_db, get_residents, add_resident, update_resident, delete_resident

st.set_page_config(page_title="디동숲", page_icon="🌳", layout="wide")
st.markdown("""<style>
.stApp {background:#ffffff;color:#000000}
h1 {color:#000000!important}
div[data-testid="stVerticalBlockBorderWrapper"] {background:#fffdf5;border-radius:18px}
div.stButton>button {border-radius:12px}
</style>""", unsafe_allow_html=True)

try:
    init_db()
    residents = get_residents()
except sqlite3.Error:
    st.error("주민 등록부를 열 수 없어요. 폴더의 쓰기 권한을 확인해 주세요.")
    st.stop()

st.title("디동숲")
st.caption(f"입주민 {len(residents)}명 · 빈집 {6-len(residents)}채")
by_house = {r["house_no"]: r for r in residents}
empty_houses = [n for n in range(1, 7) if n not in by_house]

page = st.radio(
    "화면 선택",
    ["우리 마을", "새 주민 맞이하기"],
    horizontal=True,
    key="current_page"
)

if page == "우리 마을":
    for start in (1, 4):
        columns = st.columns(3)
        for column, number in zip(columns, range(start, start + 3)):
            with column, st.container(border=True):
                st.subheader(f"🏠 {number}번 집")
                resident = by_house.get(number)
                if resident:
                    st.image(resident["avatar_svg"], width=130)
                    st.text(resident["nickname"])
                    st.caption(resident["job"])
                    if st.button("주민 만나기", key=f"visit_{number}", use_container_width=True):
                        st.session_state["selected_id"] = resident["id"]
                else:
                    st.image(
                        str(Path(__file__).with_name("empty_house.webp")),
                        width=130
                )
                st.write("아직 비어 있는 집")
    selected = next((r for r in residents if r["id"] == st.session_state.get("selected_id")), None)
    if selected:
        st.divider()
        st.subheader(f"{selected['house_no']}번 집 · 주민 기록")
        st.text(selected["nickname"])
        st.caption(f"입주일 {selected['created_at'][:10]}")
        with st.form(f"edit_{selected['id']}"):
            job = st.text_input("직업", value=selected["job"], max_chars=30)
            personality = st.text_area("성격과 소개", value=selected["personality"], max_chars=200)
            if st.form_submit_button("설정 저장"):
                try:
                    update_resident(selected["id"], job, personality)
                    st.rerun()
                except (ValueError, sqlite3.Error) as error:
                    st.error(str(error))
        with st.expander("이 주민의 퇴거 처리"):
            confirmed = st.checkbox("주민 정보와 사진을 삭제합니다.", key=f"confirm_{selected['id']}")
            if st.button("퇴거시키기", disabled=not confirmed, key=f"delete_{selected['id']}"):
                try:
                    delete_resident(selected["id"])
                    st.session_state.pop("selected_id", None)
                    st.rerun()
                except sqlite3.Error:
                    st.error("퇴거 처리에 실패했어요. 다시 시도해 주세요.")

if page == "새 주민 맞이하기":
    if not empty_houses:
        st.info("집이 다 찼어요. 주민이 퇴거하면 새로 입주할 수 있어요.")
    else:
        st.subheader("닉네임으로 주민 사진 만들기")
        with st.form("generate"):
            nickname = st.text_input("닉네임", max_chars=20, placeholder="예: 크롱")
            style_label = st.selectbox("주민 스타일", list(STYLES))
            generate = st.form_submit_button("주민 사진 만들기")
        if generate:
            # 실패한 요청이 이전 사진을 잘못 등록하게 하지 않도록 초안을 비운다.
            st.session_state.pop("draft", None)
            try:
                with st.spinner("새 이웃의 사진을 찾고 있어요…"):
                    svg = get_avatar(nickname, STYLES[style_label])
                st.session_state["draft"] = {
                    "nickname": nickname.strip(), "style": STYLES[style_label], "svg": svg}
            except ValueError as error:
                st.error(str(error))
        draft = st.session_state.get("draft")
        if draft:
            st.image(draft["svg"], width=180)
            st.text(f"입주 대기: {draft['nickname']}")
            st.caption("위 입력을 바꿨다면 ‘주민 사진 만들기’를 다시 눌러 주세요.")
            with st.form("register", clear_on_submit=False):
                house = st.selectbox("입주할 빈집", empty_houses, format_func=lambda n: f"{n}번 집")
                job = st.text_input("주민의 직업", max_chars=30, placeholder="예: 뽀로로 친구")
                personality = st.text_area("주민의 성격과 소개", max_chars=200)
                if st.form_submit_button("우리 마을에 입주시키기"):
                    try:
                        add_resident(draft["nickname"], draft["style"], draft["svg"], house, job, personality)
                        st.session_state.pop("draft", None)
                        st.rerun()
                    except (ValueError, sqlite3.Error) as error:
                        st.error(str(error))

