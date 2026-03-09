import streamlit as st
import pandas as pd

# ====================== データ定義 ======================
scales = {
    1: ("1. メジャースケール (Ionian)", [0, 2, 4, 5, 7, 9, 11], "最も基本的な長調スケール"),
    2: ("2. ナチュラルマイナースケール (Aeolian)", [0, 2, 3, 5, 7, 8, 10], "短調の基本形"),
    3: ("3. ハーモニックマイナースケール", [0, 2, 3, 5, 7, 8, 11], "7度を上げた短調"),
    4: ("4. メロディックマイナースケール（上昇形）", [0, 2, 3, 5, 7, 9, 11], "6度・7度を上げた短調"),
    5: ("5. ドリアンスケール", [0, 2, 3, 5, 7, 9, 10], "メジャーの2度モード"),
    6: ("6. フリジアンスケール", [0, 1, 3, 5, 7, 8, 10], "メジャーの3度モード"),
    7: ("7. リディアンスケール", [0, 2, 4, 6, 7, 9, 11], "メジャーの4度モード"),
    8: ("8. ミクソリディアンスケール", [0, 2, 4, 5, 7, 9, 10], "メジャーの5度モード"),
    9: ("9. ロクリアンスケール", [0, 1, 3, 5, 6, 8, 10], "メジャーの7度モード"),
    10: ("10. メジャーペンタトニックスケール", [0, 2, 4, 7, 9], "メジャーから4度・7度を除去"),
    11: ("11. マイナーペンタトニックスケール", [0, 3, 5, 7, 10], "ナチュラルマイナーから2度・6度を除去"),
    12: ("12. ディミニッシュスケール (Whole-Half)", [0, 2, 3, 5, 6, 8, 9, 11], "全音→半音の繰り返し"),
    13: ("13. コンビネーションオブディミニッシュ (Half-Whole)", [0, 1, 3, 4, 6, 7, 9, 10], "半音→全音の繰り返し")
}

# 音名変換関数
def get_note_name(semitone: int, use_flat: bool = False) -> str:
    if use_flat:
        names = ["C", "D♭", "D", "E♭", "E", "F", "G♭", "G", "A♭", "A", "B♭", "B"]
    else:
        names = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]
    return names[semitone % 12]

# ====================== Streamlitアプリ ======================
st.set_page_config(page_title="sakkyoku.info スケール変換ツール", layout="wide")
st.title("🎹 sakkyoku.info 1〜13音階 変換ツール")
st.caption("https://sakkyoku.info/theory/scale/ のスケールをドレミ表記で即表示")

tab1, tab2 = st.tabs(["📊 スケール計算機", "🔗 対応表（同じスケール関係）"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        root_display = ["C", "C♯/D♭", "D", "D♯/E♭", "E", "F", "F♯/G♭", "G", "G♯/A♭", "A", "A♯/B♭", "B"]
        root_name = st.selectbox("ルート音を選択（♯/♭対応）", root_display)
        root_semi = root_display.index(root_name)
    
    with col2:
        scale_num = st.selectbox("スケール番号（1〜13）", range(1, 14), format_func=lambda x: scales[x][0])
    
    use_flat = st.checkbox("♭表記を優先する（例: D♭ ではなく C♯）", value=False)
    
    # 計算
    name, intervals, desc = scales[scale_num]
    notes_semi = [(root_semi + i) % 12 for i in intervals]
    note_names = [get_note_name(s, use_flat) for s in notes_semi]
    
    # 結果表示
    st.subheader(f"【{name}】 ルート：{root_name}")
    st.write(desc)
    
    # 横並び表示
    st.write("**音の並び**")
    st.write(" → ".join(note_names))
    
    # 表
    df = pd.DataFrame({
        "度数": [f"{i+1}度" for i in range(len(intervals))],
        "音名": note_names,
        "セミトーン": [f"+{i}" for i in intervals]
    })
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # オクターブ上に戻る音も表示
    st.caption(f"（次のオクターブの{root_name}に戻る）")

with tab2:
    st.subheader("🔗 スケール対応表（同じ音集合・モード関係）")
    st.markdown("""
    | スケール | 同じ音集合になるスケール・関係 |
    |----------|-------------------------------|
    | **1. メジャー** | 5〜9番の全モード（開始音が違うだけ） |
    | **5. ドリアン** | 1番メジャーの2度からスタート |
    | **6. フリジアン** | 1番メジャーの3度からスタート |
    | **7. リディアン** | 1番メジャーの4度からスタート |
    | **8. ミクソ** | 1番メジャーの5度からスタート |
    | **9. ロクリアン** | 1番メジャーの7度からスタート |
    | **2. ナチュラルマイナー** | 11番マイナーペンタの親スケール |
    | **10. メジャーペンタ** | 1番メジャーから4度・7度を抜いた5音 |
    | **11. マイナーペンタ** | 2番ナチュラルマイナーから2度・6度を抜いた5音 |
    | **12・13. ディミニッシュ系** | 対称スケール（独自の音集合） |
    """)
    st.info("💡 例：ルート**ド**で1番を選ぶと、ルート**レ**で5番を選んだときと同じ7音になります（モード変換）")

st.success("これでsakkyoku.infoの1〜13スケールが全部即座に変換できます！")
st.caption("Made with ❤️ by Grok（コード自由にカスタマイズOK）")