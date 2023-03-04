import pandas as pd
from pytrends.request import TrendReq
import streamlit as st
import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots #2軸

st.set_page_config(page_title='売り上げ分析（得意先別）')
st.markdown('#### 売り上げ分析（得意先別)')

#インスタンス化
pytrends = TrendReq(hl='ja-JP', tz=-540) # timezone 時差 UTCより9時間（540分）進んでいる

def shop_fukushima():
    with st.form('設定', clear_on_submit=True):
        #福島県　全販売店
        shop_list = ['ニトリ', '東京インテリア', 'ケンポク', '丸ほん', 'ラボット', '㈱吉田家具店'] 
        #kw スペース区切り可

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

def shop_yamagata():
    with st.form('設定', clear_on_submit=True):
        #福島県　全販売店
        shop_list = ['ニトリ', '東京インテリア', '家具のオツタカ'] #kw スペース区切り可

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
            title='google trend 山形県販売店',
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

def shop_fukushima_sales():
    st.markdown('##### 検索傾向と売上の比較 福島')
    with st.form('設定', clear_on_submit=True):
        #福島県　全販売店
        shop_list = ['ケンポク', '丸ほん', 'ラボット'] #kw スペース区切り可

        shop = st.selectbox(
                '販売店を選択',
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

    #売上データ
    # ***ファイルアップロード 今期***
    uploaded_file = st.sidebar.file_uploader('今期', type='xlsx', key='now')
    df_now = pd.DataFrame()
    if uploaded_file:
        df_now = pd.read_excel(
        uploaded_file, sheet_name='受注委託移動在庫生産照会', \
            usecols=[3, 15, 16]) #index　ナンバー不要　index_col=0
        
    else:
        st.info('今期のファイルを選択してください。')
        st.stop()

    df_now['受注日2'] = df_now['受注日'].dt.strftime('%Y-%m-%d')

    s_now = pd.Series()
    if shop == 'ケンポク':
        df_now2 = df_now[df_now['得意先名']=='（有）ケンポク家具']
        s_now = df_now2.groupby('受注日2')['金額'].sum()

    elif shop == '丸ほん':
        df_now2 = df_now[df_now['得意先名']=='株式会社丸ほん']
        s_now = df_now2.groupby('受注日2')['金額'].sum() 

    elif shop == 'ラボット':
        df_now2 = df_now[df_now['得意先名']=='ラボット・プランナー株式会社']
        s_now = df_now2.groupby('受注日2')['金額'].sum() 

    # siriesのインデックスをdatetime型に変換して、date型に変換する
    s_now.index = pd.to_datetime(s_now.index)
    s_now2 = s_now.loc[start_date: end_date]

    #*******************************g_trend
    ##インスタンス化
    pytrends = TrendReq(hl='ja-JP', tz=-540) # timezone 時差 UTCより9時間（540分）進んでいる



    #集計
    pytrends.build_payload([shop], cat=0, timeframe=f'{start_date} {end_date}', geo='JP-07', gprop='')
    # category指定0　なし/
    # jp-02 青森 jp-03 岩手 jp-04 宮城 jp-05秋田 jp-06 山形 jp-07 福島/g
    # group フィルター images/youtube

    #df化
    df = pytrends.interest_over_time().drop('isPartial', axis=1).reset_index()

    df['date2'] = df['date'].dt.strftime('%Y-%m-%d')

    #**************可視化
    fig_watch = make_subplots(specs=[[{"secondary_y": True}]]) #True にすることで2つ目の軸の表示

    # 第1軸のグラフ
    fig_watch.add_trace(
        go.Scatter(x=s_now2.index, y=s_now2, name="売上"),
        secondary_y=False,
    )

    # 第2軸のグラフ
    fig_watch.add_trace(
        go.Scatter(x=df['date2'], y=df[shop], name="g_trends"),
        secondary_y=True,
    )

    fig_watch.update_yaxes(title_text="<b>primary</b> 売上", secondary_y=False)
    fig_watch.update_yaxes(title_text="<b>secondary</b> g_trends", secondary_y=True)

    st.plotly_chart(fig_watch, use_container_width=True)

def shop_yamagata_sales():
    st.markdown('##### 検索傾向と売上の比較 山形')
    with st.form('設定', clear_on_submit=True):
        #山形県　全販売店
        shop_list = ['東京インテリア', '家具のオツタカ'] #kw スペース区切り可

        shop = st.selectbox(
                '販売店を選択',
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

    #売上データ
    # ***ファイルアップロード 今期***
    uploaded_file = st.sidebar.file_uploader('今期', type='xlsx', key='now')
    df_now = pd.DataFrame()
    if uploaded_file:
        df_now = pd.read_excel(
        uploaded_file, sheet_name='受注委託移動在庫生産照会', \
            usecols=[3, 15, 16]) #index　ナンバー不要　index_col=0
        
    else:
        st.info('今期のファイルを選択してください。')
        st.stop()

    df_now['受注日2'] = df_now['受注日'].dt.strftime('%Y-%m-%d')

    s_now = pd.Series()
    if shop == '東京インテリア':
        df_now2 = df_now[df_now['得意先名']=='㈱東京ｲﾝﾃﾘｱ 山形店']
        s_now = df_now2.groupby('受注日2')['金額'].sum()

    elif shop == '家具のオツタカ':
        df_now2 = df_now[df_now['得意先名']=='㈱家具のオツタカ']
        s_now = df_now2.groupby('受注日2')['金額'].sum() 

    # siriesのインデックスをdatetime型に変換して、date型に変換する
    s_now.index = pd.to_datetime(s_now.index)
    s_now2 = s_now.loc[start_date: end_date]

    #*******************************g_trend
    ##インスタンス化
    pytrends = TrendReq(hl='ja-JP', tz=-540) # timezone 時差 UTCより9時間（540分）進んでいる



    #集計
    pytrends.build_payload([shop], cat=0, timeframe=f'{start_date} {end_date}', geo='JP-06', gprop='')
    # category指定0　なし/
    # jp-02 青森 jp-03 岩手 jp-04 宮城 jp-05秋田 jp-06 山形 jp-07 福島/g
    # group フィルター images/youtube

    #df化
    df = pytrends.interest_over_time().drop('isPartial', axis=1).reset_index()


    df['date2'] = df['date'].dt.strftime('%Y-%m-%d')

    #**************可視化
    fig_watch = make_subplots(specs=[[{"secondary_y": True}]]) #True にすることで2つ目の軸の表示

    # 第1軸のグラフ
    fig_watch.add_trace(
        go.Scatter(x=s_now2.index, y=s_now2, name="売上"),
        secondary_y=False,
    )

    # 第2軸のグラフ
    fig_watch.add_trace(
        go.Scatter(x=df['date2'], y=df[shop], name="g_trends"),
        secondary_y=True,
    )

    fig_watch.update_yaxes(title_text="<b>primary</b> 売上", secondary_y=False)
    fig_watch.update_yaxes(title_text="<b>secondary</b> g_trends", secondary_y=True)

    st.plotly_chart(fig_watch, use_container_width=True)
    

def main():
    # アプリケーション名と対応する関数のマッピング
    apps = {
        '-': None,
        '販売店_福島': shop_fukushima,
        '販売店_山形': shop_yamagata,
        'メーカー_全国': maker,
        '販売店_福島_売上比較': shop_fukushima_sales,
        '販売店_山形_売上比較': shop_yamagata_sales
  
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