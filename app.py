
from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px

import csv, re, operator
# from textblob import TextBlob

app = Flask(__name__)

person = {
	'name' : '萝卜',
	'address' : 'Wuhan, Hubei',
	'job': 'Web developer',
	'tel': '0678282923',
	'email': 'whiteluobu.com',
	'description' : '本人有着较强的沟通表达能力，对工作有上进心、认真负责、待人真诚、处人随和!换位思考有自己独特的想法这是我的优点，并且我多才多艺，我相信我能胜任任何工作!我理想就是能实现我的个人价值的挖掘，能让我的价值得到实现，同时实现企业利润和价值的化。从基层做起，不断学习，一点一滴积累经验，努力提升自我。丛基层技术做起，向管理层迈进。',
	'social_media' : [
		{
			'link': 'https://www.facebook.com/nono',
			'icon' : 'fa-facebook-f'
		},
		{
			'link': 'https://github.com/nono',
			'icon' : 'fa-github'
		},
		{
			'link': 'linkedin.com/in/nono',
			'icon' : 'fa-linkedin-in'
		},
		{
			'link': 'https://twitter.com/nono',
			'icon' : 'fa-twitter'
		}
	],
	'img': 'img/img_nono.jpg',
	'experiences' : [
		{
			'title' : 'Web Design',
			'company': 'Fiserv',
			'description' : 'Project manager and lead developer for several AZULIK websites.',
			'timeframe' : 'Apr 2018 - Now'
		},
		{
			'title' : 'Web Designer',
			'company': 'Lynden',
			'description' : 'Create Wordpress websites for small and medium companies. ',
			'timeframe' : 'Jan 2018 - Apr 2018'
		},
		{
			'title' : 'Intern - Web Design',
			'company': 'Lynden',
			'description' : 'Help to manage a 600 Sharepoint sites platform (audit, migration to Sharepoint newer versions)',
			'timeframe' : 'Aug 2017 - Dec 2017'
		}
	],
	'educations' : [
		{
			'university': 'Paris Diderot',
			'degree': 'Projets informatiques et Startégies d\'entreprise (PISE)',
			'description' : 'Gestion de projets IT, Audit, Programmation',
			'mention' : 'Bien',
			'timeframe' : '2015 - 2016'
		},
		{
			'university': 'Paris Dauphine',
			'degree': 'Master en Management global',
			'description' : 'Fonctions supports (Marketing, Finance, Ressources Humaines, Comptabilité)',
			'mention' : 'Bien',
			'timeframe' : '2015'
		},
		{
			'university': 'Lycée Turgot - Paris Sorbonne',
			'degree': 'CPGE Economie & Gestion',
			'description' : 'Préparation au concours de l\'ENS Cachan, section Economie',
			'mention' : 'N/A',
			'timeframe' : '2010 - 2012'
		}
	],
	'programming_languages' : {
		'HMTL' : ['fa-html5', '100'], 
		'CSS' : ['fa-css3-alt', '100'], 
		'SASS' : ['fa-sass', '90'], 
		'JS' : ['fa-js-square', '90'],
		'Wordpress' : ['fa-wordpress', '80'],
		'Python': ['fa-python', '70'],
		'Mongo DB' : ['fa-database', '60'],
		'MySQL' : ['fa-database', '60'],
		'NodeJS' : ['fa-node-js', '50']
	},
	'languages' : {'French' : 'Native', 'English' : 'Professional', 'Spanish' : 'Professional', 'Italian' : 'Limited Working Proficiency'},
	'interests' : ['Dance', 'Travel', 'Languages']
}

@app.route('/')
def cv(person=person):
	return render_template('MyResume.html', person=person)




@app.route('/callback', methods=['POST', 'GET'])
def cb():
	return gm1(request.args.get('data'))
def cd():
	return sm1(request.args.get('data'))

   
@app.route('/chart')
def index():
	return render_template('chartsajax.html',  graphJSON=gm(),graphJSON1=gm1())

def gm():
	df = pd.read_csv(r"static/flights.csv")
	#线性图
	fig = px.line(df,x = 'month',y = 'passengers',color="year")
	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON

def gm1(month='June'):
	df = pd.read_csv(r"static/flights.csv")
	#柱状图
	fig = px.bar(df[df['month']==month],x = 'year',y = 'passengers')
	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON


#抽烟数据分析
@app.route('/tips')
def tips():
	return render_template('tips.html',  graphJSON=sm(),graphJSON1=sm1(),graphJSON2=sm2(),graphJSON3=sm3(),graphJSON4=sm4())

def sm():
	df = pd.read_csv(r"static/tips.csv")
	fig = px.density_contour(df,x='day',y='time',color='sex')
	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON

def sm1(count='2'):
	df = pd.read_csv(r"static/tips.csv")
	fig = px.parallel_categories(df,color="size",color_continuous_scale=px.colors.sequential.Inferno)
	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON

def sm2():
	df = pd.read_csv(r"static/tips.csv")
	fig = px.box(df,x='day',y='total_bill',color='smoker',notched=True)
	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON

def sm3():
	df = pd.read_csv(r"static/tips.csv")
	fig = px.bar(df,x="sex",y="total_bill",color="smoker",barmode="group"
	  ,facet_row="time",facet_col="day",category_orders={"day": ["Thur","Fri","Sat","Sun"],"time":["Lunch", "Dinner"]})
	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON

def sm4():
	df = pd.read_csv(r"static/tips.csv")
	fig = px.histogram(df,x="sex",y="tip",histfunc="avg",color="smoker",barmode="group",
			facet_row="time",facet_col="day",category_orders={"day":["Thur","Fri","Sat","Sun"],
															 "time":["Lunch","Dinner"]})
	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON

#
@app.route('/penguins')
def penguins():
	return render_template('penguins.html',  graphJSON=pu()
		,graphJSON1=pu1()
		,graphJSON2=pu2()
		# ,graphJSON3=pu3()
		# ,graphJSON4=pu4()
		)
def pu():
	df = pd.read_csv(r"static/penguins.csv")
	fig = px.bar_polar(df,r="flipper_length_mm",theta="body_mass_g",color="sex",template="plotly_dark"
				  ,color_discrete_sequence=px.colors.sequential.Plasma_r)
	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON

def pu1():
	df = pd.read_csv(r"static/penguins.csv")
	fig = px.scatter(df,x="bill_length_mm",y="bill_depth_mm"
		   ,color="species"  # 区分颜色
		   ,size="body_mass_g"   # 区分圆的大小
		   )
	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON

def pu2():
	df = pd.read_csv(r"static/penguins.csv")
	fig = px.violin(df,x="island",y="flipper_length_mm",color="sex",box=True#显示内部箱体
		,points="all",hover_data=df.columns#结果中显示全部数据
		)
	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON

def pu3():
	df = pd.read_csv(r"static/penguins.csv")
	fig = px.scatter_polar(df,r="flipper_length_mm",theta="body_mass_g",color="island",symbol="island"
					  ,color_discrete_sequence=px.colors.sequential.Plasma_r)
	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON

# def pu4():
# 	df = pd.read_csv(r"static/penguins.csv")
# 	fig = px.scatter(df,x="bill_depth_mm",y="bill_length_mm",color="species",marginal_x="box",
# 		  marginal_y="histogram",height=600,trendline="ols",template="plotly_white")
# 	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
# 	return graphJSON

@app.route('/senti')
def main():
	text = ""
	values = {"positive": 0, "negative": 0, "neutral": 0}

	with open('ask_politics.csv', 'rt') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
		for idx, row in enumerate(reader):
			if idx > 0 and idx % 2000 == 0:
				break
			if  'text' in row:
				nolinkstext = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', '', row['text'], flags=re.MULTILINE)
				text = nolinkstext

			blob = TextBlob(text)
			for sentence in blob.sentences:
				sentiment_value = sentence.sentiment.polarity
				if sentiment_value >= -0.1 and sentiment_value <= 0.1:
					values['neutral'] += 1
				elif sentiment_value < 0:
					values['negative'] += 1
				elif sentiment_value > 0:
					values['positive'] += 1

	values = sorted(values.items(), key=operator.itemgetter(1))
	top_ten = list(reversed(values))
	if len(top_ten) >= 11:
		top_ten = top_ten[1:11]
	else :
		top_ten = top_ten[0:len(top_ten)]

	top_ten_list_vals = []
	top_ten_list_labels = []
	for language in top_ten:
		top_ten_list_vals.append(language[1])
		top_ten_list_labels.append(language[0])

	graph_values = [{
					'labels': top_ten_list_labels,
					'values': top_ten_list_vals,
					'type': 'pie',
					'insidetextfont': {'color': '#FFFFFF',
										'size': '14',
										},
					'textfont': {'color': '#FFFFFF',
										'size': '14',
								},
					}]

	layout = {'title': '<b>意见挖掘</b>'}

	return render_template('sentiment.html', graph_values=graph_values, layout=layout)


if __name__ == '__main__':
  app.run(debug= True,port=5000,threaded=True)
