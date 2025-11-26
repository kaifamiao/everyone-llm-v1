cumstom_css="""
<style>
#MainMenu {visibility: hidden;}
MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stButton > button {
    color: #0d6cf9;
    align: left;
    # background-color: #ffffff;
    background-color: #e8f2fc;
    #background-color: #0d6cf9;
    border-color: #9ec5fe;
    display: inline-block;
    font-weight: 400;
    text-align: center;
    vertical-align: middle;
    user-select: none;
    border: 1px solid transparent;
    padding: .375rem .75rem;
    font-size: 1rem;
    line-height: 1.5;
    border-radius: .25rem;
    transition: color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out;
    width: 100%;
    display: inline-block;
    /*圆角*/
    border-radius: 5px;
}
.stButton > button:hover {
    color: #0a58ca;
    background-color: #9ec5fe;
    border-color: #6ea8fe;
}
.stButton > knowledge> button:active {
    color: #0a58ca;
    background-color: #6ea8fe;
    border-color: #9ec5fe;
}
/* 侧边栏设置 */
[data-testid="stSidebar"] {
    background-color: white;  /* 设置背景颜色 */
    padding: 20px;
    height: 100vh;              /* 使侧边栏占满整个视口高度 */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;           /* 隐藏滚动条 */

}
[data-testid="stSidebar"] .top-section {
    background-color: blue;  /* 设置底部按钮的背景颜色 */
    border: #4CAF50 2px solid;
    flex-grow: 1;
    padding: 10px;
    border-radius: 10px;
    overflow: hidden;           /* 隐藏滚动条 */
}
</style>
"""