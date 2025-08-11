import streamlit as st
import pandas as pd
import joblib
import sys
import time
import warnings

# 设置网页标题
st.set_page_config(page_title="LARS 风险预测小工具", layout="wide")
st.title("LARS 风险预测小工具")

# 添加进度指示器
progress_bar = st.progress(0)
status_text = st.empty()

# 环境信息
status_text.text("正在检查环境...")
progress_bar.progress(10)
st.subheader("环境信息")
st.write(f"Python 版本: {sys.version.split()[0]}")

try:
    st.write(f"Streamlit 版本: {st.__version__}")
except:
    st.warning("无法获取Streamlit版本")

# 模型加载
status_text.text("正在加载模型...")
progress_bar.progress(30)
st.subheader("模型加载状态")
model_path = 'lars_risk_model.pkl'
model_loaded = False

try:
    with st.spinner("模型加载中，请稍候..."):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model = joblib.load(model_path)
    st.success("✅ 模型加载成功！")
    model_loaded = True
    progress_bar.progress(50)
except Exception as e:
    st.error(f"❌ 模型加载失败: {str(e)}")
    st.warning("预测功能将不可用，请检查模型文件是否存在")
    # 显示文件列表
    try:
        import os
        st.write("当前目录文件:", os.listdir('.'))
    except:
        pass

# 输入区域
status_text.text("正在准备输入界面...")
progress_bar.progress(70)
st.sidebar.header("请输入以下特征：")

age = st.sidebar.number_input("年龄 (岁)", min_value=0.0, max_value=120.0, value=50.0, step=1.0)
BMI = st.sidebar.number_input("BMI (kg/m²)", min_value=10.0, max_value=50.0, value=22.0, step=0.1)
tumor_dist = st.sidebar.number_input("肿瘤距离 (cm)", min_value=0.0, max_value=50.0, value=5.0, step=0.1)
surg_time = st.sidebar.number_input("手术时间 (分钟)", min_value=0.0, max_value=600.0, value=180.0, step=1.0)
exhaust = st.sidebar.number_input("排气天数 (天)", min_value=0.0, max_value=30.0, value=2.0, step=0.5)
tumor_size = st.sidebar.number_input("肿瘤大小 (cm)", min_value=0.1, max_value=20.0, value=3.0, step=0.1)
TNM = st.sidebar.number_input("TNM 分期 (数值)", min_value=1.0, max_value=4.0, value=2.0, step=1.0)
neoadjuvant = st.sidebar.number_input("是否新辅助治疗 (0=否, 1=是)", min_value=0.0, max_value=1.0, value=0.0, step=1.0)# 预测功能
progress_bar.progress(90)
if model_loaded:
    if st.button("点击预测"):
        try:
            input_data = pd.DataFrame([[age, BMI, tumor_dist, surg_time, exhaust, tumor_size, TNM, neoadjuvant]],
                                     columns=['age', 'BMI', 'tumor_dist', 'surg_time', 'exhaust', 'tumor_size', 'TNM', 'neoadjuvant'])
            
            with st.spinner("预测中..."):
                prediction = model.predict(input_data)[0]
                time.sleep(1)  # 模拟处理时间
            
            if prediction == 1:
                st.success("✅ 预测结果：存在风险")
                st.markdown("**建议:** 请咨询专业医生进行进一步评估，定期复查")
            else:
                st.info("❌ 预测结果：无明显风险")
                st.markdown("**建议:** 继续保持健康生活习惯，定期体检")
                
        except Exception as e:
            st.error(f"预测失败: {str(e)}")
else:
    st.warning("模型未加载，无法进行预测")

# 完成初始化
progress_bar.progress(100)
status_text.text("应用已就绪")
time.sleep(1)
status_text.empty()
progress_bar.empty()

# 使用说明
st.sidebar.markdown("---")
st.sidebar.subheader("使用说明")
st.sidebar.info("1. 输入特征值\n2. 点击预测按钮\n3. 查看结果")
