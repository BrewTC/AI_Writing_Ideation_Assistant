import streamlit as st
import os
from openai import OpenAI
# from dotenv import load_dotenv
import base64

# --- 初始化環境 ---
# load_dotenv()
# api_key = os.getenv("API_KEY")  # 確認在 .env 文件中正確地定義 API 金鑰

# 從 Streamlit Secrets 讀取安全的 API Key
api_key = st.secrets["API_KEY"]
api_base_url = st.secrets["API_BASE_URL"]

# 設定頁面屬性
st.set_page_config(page_title="AI 寫作發想助理", page_icon="💡", layout="wide")

# --- 自訂 CSS ---
# 以 HTML & CSS 方式置中標題、文本框和按鈕
st.markdown(
    """
    <style>
    /* 置中內容 */
    .main-content {
        text-align: center;
    }
    /* 文本框置中 */
    .center-text-area textarea {
        margin: 0 auto;
        display: block;
    }
    /* 按鈕置中 */
    div.stButton > button {
        margin: 0 auto;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True
)

# --- 定義中心化區塊 ---
st.markdown('<div class="main-content">', unsafe_allow_html=True)  # 標記開始置中
st.title("AI 寫作發想助理")
# 響應式封面圖片
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

image_base64 = get_base64_image("img/123.jpg")

st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/jpeg;base64,{image_base64}" alt="封面圖片" style="width: 100%; max-width: 600px; height: auto;">
    </div>
    """,
    unsafe_allow_html=True
)
st.caption("貼上您的草稿，選擇一項 AI 輔助功能，激盪更多靈感。")

# --- 定義 Prompt 選項 ---
prompts = {
    "文章解析": """
請依照以下指示，對我的文件檔案進行「摘要」：

- 具體且注重細節，以最高解析度整理內容，提供實際例子。
- 具體的細節都不可以省略，要留下內容的所有人事時地物、器具、物品、地點、英文原文...等所有資訊。不要因為重寫就讓原本的材料解析度消失了。

---

<輸出內容>
{摘要}

- 其它資訊
{讀者人群樣貌}
{讀者人群可能在什麼場景？需要解決痛點請列出五個}
{他們常有的痛點是什麼？最少列十個}
{看完文章可以滿足他們那些需求？最少列十個}
</輸出內容>
""",
    "萬能寫作": """
請你使用萬能寫作法，來把我上述的材料改寫成有結構的段落
（方法來源：師北辰．《讓寫作成為自我精進的武器》）

▋ {重點}

{一句話主題}
{故事／範例／理論／內容展開}
{一句話總結}

- 不要有寫入或出現任何{重點}當中的任何文字
- 我提供的【架構】只是一種摘要式的概念，每句話之間有非常多需要補足的地方，請你幫我把內容寫得更完整一點。
- 使用每寫完一兩句話就換行的排版
- 具體的細節都不可以省略，要留下內容的所有人事時地物、器具、物品、地點、英文原文...等所有資訊。不要因為重寫就讓原本的材料解析度消失了。

- 你現在的寫作對象只寫給一個人，那就是「兩年前的自己」。你當然不是真的對著兩年前的自己說話，不要提到任何「過去的我們、兩年前的我們...」之類的用語，而是用一種好似跟著兩年前的自己說話的親切語氣，跟讀者說話。
""",
    "文章軸心": """
好，現在我們使用《軸心三問》進行收斂

這篇文章的讀者是誰，他們的快樂極端值是什麼？
讀完這篇文章，他們可以得到什麼？
沒有讀這篇文章，他們會有什麼痛點沒有解決？

- 請在對話中將上面的文章軸心內容以列點的方式具體說明
""",
    "文章標題": """
---
第一個任務:請根據以上內容的方向與目標受眾，幫我創作 5 個「極度具體」的標題版本，並符合以下條件：

1）透過以下方式增加「具體性」：  
  - 使用明確數字／指標（不是「提升流量」，而是「流量提升 47%」）  
  - 精準定義目標讀者（不是「企業主」，而是「員工少于 5 人的女性創業者」）  
  - 具體時間範圍（不是「快速見效」，而是「14 天內見效」）  
  - 精確描述克服的障礙（不是「適合所有人」，而是「即使失敗三次」）  
  - 描述具體使用情境（不是「幫助你更專注」，而是「在你每天通勤時幫你專注」）
	- 使用方法命名（不是「五種思考方法幫助獲得獨特觀點」，而是「靈感發電機」）

一個標題只使用兩個具體性元素，不要再多。

2）對每個版本，請說明：  
  • 你加入了哪兩個「具體性」元素？  
  • 為什麼這樣讓標題更吸引人？  
  • 哪一群特定讀者會覺得這個標題是專門為他們寫的？

請讓我的標題像是「為那個人量身打造的」一樣精準貼切！

---

第二個任務:
請你根據我們上述的原始材料，依照「爆款標題 10 大策略」中提到「下標題」的技巧，進行下標題。

<爆款標題 10 大策略>
1. 直白陳列法
2. 原生爆點法
3. 一句話法
4. 反常理
5. 數字
6. 熟悉＋驚喜（俗語改編）
7. 對比
8. 對話
</爆款標題 10 大策略>

## 輸出格式

⇨ 下標題方法
【 標題示例 1 】
【 標題示例 2 】
【 標題示例 3 】

## 規則

1. 分析我提供的原始材料內容，提煉核心價值點。
2. 對生成的標題進行優化，提升吸引力和傳播力。
3. 題用語杜絕煽情，以冷靜、誠懇語氣寫作。

---

請把二個任務的結果直接在對話視窗，呈現內容，當中用分隔線，分開表示二個任務「標題內容」
""",
    "文章前言": """
我要訓練你成為一台「Hook（鉤子）」寫作機器。

這裡有7段被稱為「Hook」的文字範本—

<我幫你看了這本書>
Jon Youshaei，前 YouTube 創作者行銷總監，人稱「地表上最聰明的創作者」。
他在前年創造了 2.6 億次觀看，平均每天 70 萬，完全不靠運氣，只靠驗證過有效、可複製的策略。
在 Jay Cluse 的播客中，他詳細說明自己如何測試新內容、找到自己的定位，以及他對 YouTube 未來發展的看法。
Youshaei：「所有創作者都應該問自己一個問題：我的個人秀會長怎樣？」
</我幫你看了這本書>

<我幫你做完了最難的事>
Mr. Beast，人稱 YouTube 之王，史上最高流量的 YouTuber。
在過去短短十二個月內，他新增了五千萬名訂閱者。
我狂看了一百小時他的影片，只為了研究他到底怎麼辦到的。
Mr. Beast：「所有人都會覺得你是瘋子，直到你成功的那天。」
以下，就是他用來快速成長的三大框架（你可以直接套用在任何平台上）：
1. {框架1}
2. {框架2}
3. {框架3}
</我幫你做完了最難的事>

<我幫你付了錢所以你不用付了>
我花了二十萬美元請 Patrick Bet-David 給我諮詢，
最後我靠他的協助，打造了一家十億美元公司。
這是我學到的七個重點：
</我幫你付了錢所以你不用付了>

<簡單但強大>
過去一年裡，我在脆上發表了數百條簡短（但強大）的寫作技巧。
其中這 19 條，累積超過一百萬次瀏覽，還有上千個留言與分享。
現在我把它全部整理在這裡——
</簡單但強大>

<今非昔比>
「2019年時，我在 LinkedIn 上根本沒人認識。現在，我可以幫別人在三個月內增加一萬名粉絲。」
</今非昔比>

<筆記文模板>
Jenny Hoyos ，一位拉丁裔 18 歲小女生，徹底破解了短影音製作方法，她的頻道有兩百萬訂閱，平均每隻短影音都有一千萬次觀看，單隻短影音最高觀看 8182 萬次。
她不賣肉，不買粉，全靠自己的創意。在 Jay Clouse 訪談中，她詳細說明了她是怎樣做到的。
她說：「我可以讓任何事情爆紅，一切只是『故事＋轉折』。」
以下是她的作法。
</筆記文模板>

<我幫你整理資料>
GPT-5 終於來了，整個網路都為之瘋狂。
為了讓你在最短的時間快速了解 GPT-5，這篇文章，我把 OpenAI 官方、Ethan Mollick、Latent.Space 等五份我挑選出來的創作者文章和影片完整吸收，提煉出八個關鍵啟發點：
</我幫你整理資料>

針對剛剛對話中產出的內容，我要你用上面這段示範文字的元素，寫出：
3 個「我幫你看了這本書」類型的 Hook。
3 的「我幫你做完了最難的事」類型的 Hook。
3 的「我幫你付了錢所以你不用付了」類型的 Hook。
3 的「簡單但強大」類型的 Hook。
3 的「今非昔比」類型的 Hook。
3 的「筆記文模板」類型的 Hook。
3 的「我幫你整理資料」類型的 Hook。

請你將每個產出版本都進行編號：A-1, A-2....

寫這種 Hook 最關鍵的地方，在於最後一句一定要讓讀者有點擊、想看下去的動力。怎麼做到？

• 非常具體地告訴讀者你要給他什麼（比如「一個手把手步驟指南」或「保證可執行的計畫」等）。
• 對結果要非常具體，給出具體的名詞導向結果（例如「...教你買下人生第一間台北蛋黃區房子」），不要用抽象、形容詞導向的結果（像是「...讓你過上幸福人生」）。
• 不要說「我們」。這個故事要用「你」，以個人角度對讀者說話。
- 我提供的範例只是一種摘要式的概念，每句話之間可能還有沒補足的地方，請你幫我把故事寫得更完整一點，至少十句話。
""",
    "啟發性分析": """
請依照以下指示，對我的文件檔案進行「啟發性分析」：

- 具體且注重細節，以文章中十個最啟發性的內容，整理成列點式的重點。
- 具體的細節都不可以省略，要留下內容的所有人事時地物、器具、物品、地點、英文原文...等所有資訊。不要因為重寫就讓原本的材料解析度消失了。
- 不要建立新文件，不要自己建立。
- 請針對我給你的資料內容或是補充提示，詳細整理。
- 原文中沒有的內容，請不要擅自捏造任何不存在的資訊。

{輸出內容在對話中呈現}
""", 
}

st.markdown('</div>', unsafe_allow_html=True)  # 標記置中結束

# --- 使用者輸入 & 功能選項 ---
st.markdown('<div class="main-content center-text-area">', unsafe_allow_html=True)  # 文本區塊置中
user_input = st.text_area("✍️ 輸入您的文章內容", height=250, placeholder="在這裡貼上您的文章內容...")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="main-content">', unsafe_allow_html=True)  # 功能選擇置中
action_key = st.selectbox("🔧 選擇功能", list(prompts.keys()))
st.markdown("💡 建議流程：")
st.markdown("撰寫筆記 → 文章解析 → 修正 → 萬能寫作 → 文章軸心 → 文章標題 → 文章前言")
st.markdown('</div>', unsafe_allow_html=True)

# --- 呼叫 Gemini API ---
def call_generative_ai(prompt_text):
    """呼叫 Gemini 模型並獲取生成結果"""
    if not api_key:
        st.error("❌ 未設定 API Key，請檢查 .env 檔案中的 API_KEY 變數。")
        return None

    # 初始化 OpenAI 客戶端
    client = OpenAI(
        api_key=api_key,
        base_url=api_base_url  # 從 st.secrets 讀取的 Base URL
		
    #     api_key=api_key,  # 使用你的 Gemini API Key
    #     base_url=""  # Gemini API Base URL
    )

    try:
        # 發送聊天請求到 Gemini 模型
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_text}
            ]
        )

        # 返回結果
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"❗ 發生錯誤：{str(e)}")
        return None

# --- 生成按鈕 ---
if st.button("🚀 開始生成"):
    if not user_input.strip():
        st.warning("請先輸入文章內容再執行。")
    else:
        prompt_text = f"{prompts[action_key]}\n\n---\n\n以下是我的文件內容：\n{user_input}"
        with st.spinner("AI 正在生成中，請稍候..."):
            result_text = call_generative_ai(prompt_text)

        if result_text:
            st.text_area("✅ AI 生成結果", value=result_text, height=300)
            st.success("生成完成！")
        else:
            st.error("⚠️ 生成失敗，請檢查 API Key 或回應格式。")
