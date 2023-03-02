import pandas as pd
from pytrends.request import TrendReq
import streamlit as st
import datetime
import plotly.graph_objects as go

st.set_page_config(page_title='売り上げ分析（得意先別）')
st.markdown('#### 売り上げ分析（得意先別)')

#インスタンス化
pytrends = TrendReq(hl='ja-JP', tz=-540) # timezone 時差 UTCより9時間（540分）進んでいる

def shop_fukushima_all():
    with st.form('設定', clear_on_submit=True):
        #福島県　全販売店
        shop_list = ['ニトリ', '東京インテリア', 'ケンポク', '丸ほん', 'ラボット'] #kw スペース区切り可

        kw_list = st.multiselect(
                '販売店を選択(複数可)',
                shop_list
                )

        # 集計する期間の設定
        start_date = st.date_input(
            "開始時期",
            datetime.date(2023, 1, 1))

        end_date = st.date_input(
            "終了時期",
            datetime.date.today())
        
        submitted = st.form_submit_button("データ収集")

    # start_date, end_date = "2023-01-01", "2023-02-28"
    if submitted:
        #集計
        pytrends.build_payload(kw_list, cat=0, timeframe=f'{start_date} {end_date}', geo='JP-07', gprop='')
        # category指定0　なし/
        # jp-02 青森 jp-03 岩手 jp-04 宮城 jp-05秋田 jp-06 山形 jp-07 福島/g
        # group フィルター images/youtube

        #df化
        df = pytrends.interest_over_time().drop('isPartial', axis=1).reset_index()

        #可視化
        #グラフを描くときの土台となるオブジェクト
        fig = go.Figure()
        #今期のグラフの追加
        for col in df.columns[1:]:

            fig.add_trace(
                go.Scatter(
                    x=df['date'],
                    y=df[col],
                    #   mode = 'lines+markers+text', #値表示
                    #   text=df[col],
                    #   textposition="top center",
                    name=col
                    )
            )

        #レイアウト設定     
        fig.update_layout(
            title='google trend 福島県販売店',
            showlegend=True #凡例表示
        )
        #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.stop() 

def maker():
    st.markdown('##### メーカー分析 全国')

    with st.form('設定', clear_on_submit=True):

        # 集計する期間の設定
        start_date = st.date_input(
            "開始時期",
            datetime.date(2023, 1, 1))

        end_date = st.date_input(
            "終了時期",
            datetime.date.today())
        
        all_list = ['カリモク', '飛騨産業', '柏木工', 'シラカワ', '日進木工', 'マスターウォール', \
                    '浜本工芸', 'ナガノインテリア', 'フジファニチュアー', '関家具', 'フクラ', '高野木工', \
                    '宮崎椅子']
        selected_list = st.multiselect(
                'メーカーを選択(複数可)',
                all_list
                )
        
        
        submitted = st.form_submit_button("データ収集")

    kw_list3 = ['カリモク', '飛騨産業', '柏木工', 'シラカワ', '日進木工'] #kw スペース区切り可 カリモク入れると全部0になる
    kw_list4 = ['カリモク', 'マスターウォール', '浜本工芸', 'ナガノインテリア', 'フジファニチュアー']
    kw_list5 = ['カリモク', '関家具', 'フクラ', '高野木工', '宮崎椅子']

    maker_list =[kw_list3, kw_list4, kw_list5] 

    df_maker = pd.DataFrame(columns=['total'])
    for maker in maker_list:

        #集計
        pytrends.build_payload(maker, cat=0, timeframe=f'{start_date} {end_date}', geo='JP', gprop='')
        #df化
        df3 = pytrends.interest_over_time().drop('isPartial', axis=1).reset_index()
        df3.loc['total'] =df3.sum()
        df3_sum = df3.T
        df3_sum = df3_sum[['total']].drop(index= 'date', axis=0)

        df_maker = pd.concat([df_maker, df3_sum], join='inner')

    df_maker = df_maker.drop_duplicates() #重複行の削除　カリモク
    df_maker = df_maker.sort_values('total', ascending=False)
    df_maker['total'] = df_maker['total'].astype('int')
    
    df_maker_selected = df_maker.loc[selected_list]
    df_maker_selected = df_maker_selected.sort_values('total', ascending=False)

    #可視化
    #グラフを描くときの土台となるオブジェクト
    fig = go.Figure()
    #今期のグラフの追加

    num = 0
    for maker in df_maker_selected.index:

        fig.add_trace(
            go.Bar(
                x=[maker],
                y=[df_maker_selected.iat[num, 0]],
                # mode = 'lines+markers+text', #値表示
                text=str(df_maker_selected.iat[num, 0]),
                textposition="outside",
                name=maker
                )
        )
        num += 1

    #レイアウト設定     
    fig.update_layout(
        title='google trend メーカー名/全国',
        showlegend=True #凡例表示
    )
    #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
    st.plotly_chart(fig, use_container_width=True)






def main():
    # アプリケーション名と対応する関数のマッピング
    apps = {
        '-': None,
        '販売店_福島': shop_fukushima_all,
        'メーカー_全国': maker

  
    }
    selected_app_name = st.sidebar.selectbox(label='分析項目の選択',
                                             options=list(apps.keys()))

    if selected_app_name == '-':
        st.info('サイドバーから分析項目を選択してください')
        st.stop()

    link = '[home](http://linkpagetest.s3-website-ap-northeast-1.amazonaws.com/)'
    st.sidebar.markdown(link, unsafe_allow_html=True)
    st.sidebar.caption('homeに戻る')    

    # 選択されたアプリケーションを処理する関数を呼び出す
    render_func = apps[selected_app_name]
    render_func()

if __name__ == '__main__':
    main()