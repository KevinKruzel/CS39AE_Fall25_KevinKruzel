import streamlit as st

st.title("👋 My Bio")

# ---------- TODO: Replace with your own info ----------
NAME = "Kevin Kruzel"
PROGRAM = "Mathematics"
INTRO = (
    "My name is Kevin Kruzel and I am a Mathematics Major loooking to graduate this semester."
    "Data visualization excites me because it allows us to see the data in new and interesting ways."
)
FUN_FACTS = [
    "I love playing video and tabletop games.",
    "I currently have 6 pets.",
    "My favorite color is blue.",
]
PHOTO_PATH = "assets/your_photo.jpg"  # Put a file in repo root or set a URL

# ---------- Layout ----------
col1, col2 = st.columns([1, 2], vertical_alignment="center")

with col1:
    try:
        st.image(PHOTO_PATH, caption=NAME, use_container_width=True)
    except Exception:
        st.info("Add a photo named `your_photo.jpg` to the repo root, or change PHOTO_PATH.")
with col2:
    st.subheader(NAME)
    st.write(PROGRAM)
    st.write(INTRO)

st.markdown("### Fun facts")
for i, f in enumerate(FUN_FACTS, start=1):
    st.write(f"- {f}")

st.divider()
st.caption("Edit `pages/1_Bio.py` to customize this page.")
