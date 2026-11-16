import streamlit as st
from PIL import Image
import google.generativeai as genai

# 페이지 설정
st.set_page_config(
    page_title="홈닥터 AI - 자가 수리 도우미",
    page_icon="🔧",
    layout="centered",
)

# 상단 타이틀
st.title("🔧 홈닥터 AI - 일상 고장 자가 수리 도우미")
st.write("고장 난 곳을 사진으로 찍어 올려주시면 초보자도 쉽게 고치는 법을 알려드려요!")

# 안전 안내 배너
st.warning(
    "⚠️ **안전 주의 안내**: 전기 누전, 심각한 가스 누출, 대규모 수도 누수 등 위험한 상황일 때는 직접 수리하지 마시고 즉시 전문가를 호출하세요."
)

st.markdown("---")

# 사이드바 설정 (API 키 입력)
st.sidebar.header("🔑 설정")
api_key = st.sidebar.text_input(
    "Google Gemini API 키 입력",
    type="password",
    help="Google AI Studio에서 무료로 발급받은 API 키를 입력하세요.",
)

# 메인 입력부
st.subheader("1️⃣ 고장 부위 사진과 증상을 알려주세요")
uploaded_file = st.file_uploader(
    "고장 난 부위 사진 선택 (JPG, PNG)", type=["jpg", "jpeg", "png"]
)

symptom_text = st.text_input(
    "증상 한 줄 입력 (선택사항)",
    placeholder="예: 싱크대 물이 안 내려가고 꽉 막혔어요.",
)

if uploaded_file is not None:
  # 업로드된 이미지 표시
  image = Image.open(uploaded_file)
  st.image(image, caption="업로드된 고장 부위 사진", use_container_width=True)

# 진단하기 버튼
if st.button("🔍 AI 수리 방법 진단하기", type="primary"):
  if not api_key:
    st.error(
        "❌ 사이드바에 Google Gemini API 키를 먼저 입력해 주세요! (무료 발급"
        " 가능)"
    )
  elif not uploaded_file:
    st.error("❌ 분석할 고장 부위 사진을 업로드해 주세요.")
  else:
    with st.spinner("🤖 홈닥터 AI가 고장 상태를 꼼꼼히 진단하고 있습니다..."):
      try:
        # Gemini API 설정
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")

        # 프롬프트 작성
        prompt = f"""
                당신은 친절하고 전문적인 '홈닥터 AI (자가 수리 도우미)'입니다.
                사용자가 업로드한 고장 부위 사진과 추가 증상 설명을 분석하여, 초보자도 쉽게 따라 할 수 있는 자가 수리 가이드를 작성해 주세요.
                
                추가 증상 설명: {symptom_text if symptom_text else "없음 (사진 위주로 분석)"}
                
                반드시 아래 양식에 맞춰 한국어로 답변해 주세요:
                
                1. 🔍 예상 원인: (고장 난 원인을 알기 쉽게 1~2문장으로 설명)
                2. 🧰 필요한 준비물: (집에 있거나 쉽게 구할 수 있는 도구 및 재료 목록)
                3. 📋 3단계 수리 순서:
                   - 1단계: (...)
                   - 2단계: (...)
                   - 3단계: (...)
                4. ⚠️ 주의사항: (수리 중 다치지 않도록 주의할 점)
                """

        # AI 호출
        response = model.generate_content([image, prompt])

        # 결과 출력
        st.success("✨ 진단이 완료되었습니다!")
        st.markdown("### 📋 AI 맞춤형 수리 가이드")
        st.markdown(response.text)

      except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
        st.info(
            "💡 API 키가 올바른지, 혹은 인터넷 연결 상태를 다시 한번 확인해"
            " 주세요."
        )
