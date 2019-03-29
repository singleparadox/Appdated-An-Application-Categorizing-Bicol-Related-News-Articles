import generate_model as gm
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.manifold import MDS
from sklearn.metrics.pairwise import cosine_similarity
import json
import random
import numpy as np
import datetime
from calendar import monthrange
import os

def show_plots():
    dist = 1 - cosine_similarity(gm.X3)

    MDS()

    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)

    pos = mds.fit_transform(dist)

    xs, ys = pos[:, 0], pos[:, 1]

    with open("selected_model.txt") as f:
        text = f.read()
        a = text.strip()
        file_name = os.path.basename(a)
        no_extension = os.path.splitext(file_name)[0]

    if not os.path.exists("cluster_labels/"+no_extension+".txt"):
        temp = ""
        with open("cluster_labels/"+no_extension+".txt",'w+') as file:
            for s in range(0, gm.kmeans.n_clusters):
                temp += "\""+str(s)+"\": \"No Label\","
            tmp = temp[:-1]
            file.write("{"+tmp+"}")

    #Open Cluster Names Dictionary
    cluster_dict = []
    with open("cluster_labels/"+no_extension+".txt") as f:
            text = f.read()
            if text == '':
                temp = ""
                for s in range(0, gm.kmeans.n_clusters):
                    temp += "\""+str(s)+"\": \"No Label\","
                tmp = "{"+temp[:-1]+"}"
                text = tmp
            cluster_dict = json.loads(text)    
    cluster_names = cluster_dict

    #Generate Random Colors
    cluster_colors = {}
    for x in range(0,len(cluster_names)):
        cluster_colors[x] = "#%06x" % random.randint(0, 0xFFFFFF)


    clusters = gm.clusters #fc.ya

    df = pd.DataFrame(dict(x=xs, y=ys, label=clusters)) 

    groups = df.groupby('label')


    fig, ax = plt.subplots(figsize=(17, 9)) # set size
    ax.margins(0.05) #padding to the autoscaling

    for name, group in groups:
        ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, 
                label=cluster_names[str(name)], color=cluster_colors[name], 
                mec='none')
        ax.set_aspect('auto')
        ax.tick_params(\
            axis= 'x',         
            which='both',    
            bottom='off',   
            top='off',        
            labelbottom='off')
        ax.tick_params(\
            axis= 'y',       
            which='both',    
            left='off',     
            top='off',       
            labelleft='off')
        
    ax.legend(numpoints=1)


    for i in range(len(df)):
        ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['label'], size=8)  

    plt.show()



def show_month():                                                
	df_with_clusters = pd.read_csv("main_with_clusters.csv")

	with open("selected_model.txt") as f:
		text = f.read()
		a = text.strip()
		file_name = os.path.basename(a)
		no_extension = os.path.splitext(file_name)[0]

	if not os.path.exists("cluster_labels/"+no_extension+".txt"):
		temp = ""
		with open("cluster_labels/"+no_extension+".txt",'w+') as file:
			for s in range(0, gm.kmeans.n_clusters):
				temp += "\""+str(s)+"\": \"No Label\","
			tmp = temp[:-1]
			file.write("{"+tmp+"}")

	df_with_clusters['date'] = pd.to_datetime(df_with_clusters['date'], format='%Y-%m-%d', errors='ignore')
	with open("cluster_labels/"+no_extension+".txt") as f:
			text = f.read()
			if text == '':
				temp = ""
				for s in range(0, gm.kmeans.n_clusters):
					temp += "\""+str(s)+"\": \"No Label\","
				tmp = "{"+temp[:-1]+"}"
				text = tmp
			cluster_dict = json.loads(text)    
	cluster_names = cluster_dict

	clusters = []

	for x in range(0, gm.kmeans.n_clusters):
		clusters.append(df_with_clusters.loc[df_with_clusters['cluster'] == x])

	now = datetime.datetime.now()

	this_year = str(now.year)

	jan = []
	feb = []
	mar = []
	apr = []
	may = []
	jun = []
	jul = []
	aug = []
	sep = []
	oct_ = []
	nov = []
	dec_ = []


	for x in range(0, len(clusters)):
		for y in range(1, 13):
			if y == 1:
				month_range = monthrange(int(this_year)-1, y)
				temp_ = clusters[x].loc[clusters[x]['date'].between(str(int(this_year)-1)+'-'+str("{:02d}".format(12))+'-'+str(month_range[1]),this_year+'-'+str("{:02d}".format(y+1))+'-'+str(1), inclusive=False)]
				jan.append([x,len(temp_)])
			elif y == 2:
				month_range = monthrange(int(this_year), y)
				temp_ = clusters[x].loc[clusters[x]['date'].between(this_year+'-'+"{:02d}".format(y-1)+'-'+str(monthrange(int(this_year),y-1)[1]),this_year+'-'+"{:02d}".format(y)+'-'+str(monthrange(int(this_year),y)[1]), inclusive=False)]
				#print(this_year+'-'+"{:02d}".format(y-1)+'-'+str(monthrange(int(this_year),y-1)[1]),this_year+'-'+"{:02d}".format(y)+'-'+str(monthrange(int(this_year),y)[1]))
				feb.append([x,len(temp_)])
			elif y == 3:
				month_range = monthrange(int(this_year), y)
				temp_ = clusters[x].loc[clusters[x]['date'].between(this_year+'-'+"{:02d}".format(y-1)+'-'+str(monthrange(int(this_year),y-1)[1]),this_year+'-'+"{:02d}".format(y)+'-'+str(monthrange(int(this_year),y)[1]), inclusive=False)]
				#print(this_year+'-'+"{:02d}".format(y-1)+'-'+str(monthrange(int(this_year),y-1)[1]),this_year+'-'+"{:02d}".format(y)+'-'+str(monthrange(int(this_year),y)[1]))
				mar.append([x,len(temp_)])
			elif y == 4:
				month_range = monthrange(int(this_year), y)
				temp_ = clusters[x].loc[clusters[x]['date'].between(this_year+'-'+"{:02d}".format(y-1)+'-'+str(monthrange(int(this_year),y-1)[1]),this_year+'-'+"{:02d}".format(y)+'-'+str(monthrange(int(this_year),y)[1]), inclusive=False)]
				#print(this_year+'-'+"{:02d}".format(y-1)+'-'+str(monthrange(int(this_year),y-1)[1]),this_year+'-'+"{:02d}".format(y)+'-'+str(monthrange(int(this_year),y)[1]))
				apr.append([x,len(temp_)])
			elif y == 5:
				month_range = monthrange(int(this_year), y)
				temp_ = clusters[x].loc[clusters[x]['date'].between(this_year+'-'+"{:02d}".format(y-1)+'-'+str(monthrange(int(this_year),y-1)[1]),this_year+'-'+"{:02d}".format(y)+'-'+str(monthrange(int(this_year),y)[1]), inclusive=False)]
				#print(this_year+'-'+"{:02d}".format(y-1)+'-'+str(monthrange(int(this_year),y-1)[1]),this_year+'-'+"{:02d}".format(y)+'-'+str(monthrange(int(this_year),y)[1]))
				may.append([x,len(temp_)])
			elif y == 6:
				month_range = monthrange(int(this_year), y)
				temp_ = clusters[x].loc[clusters[x]['date'].between(this_year+'-'+"{:02d}".format(y-1)+'-'+str(monthrange(int(this_year),y-1)[1]),this_year+'-'+"{:02d}".format(y)+'-'+str(monthrange(int(this_year),y)[1]), inclusive=False)]
				#print(this_year+'-'+"{:02d}".format(y-1)+'-'+str(monthrange(int(this_year),y-1)[1]),this_year+'-'+"{:02d}".format(y)+'-'+str(monthrange(int(this_year),y)[1]))
				jun.append([x,len(temp_)])
			elif y == 7:
				month_range = monthrange(int(this_year), y)
				temp_ = clusters[x].loc[clusters[x]['date'].between(this_year+'-'+"{:02d}".format(y-1)+'-'+str(monthrange(int(this_year),y-1)[1]),this_year+'-'+"{:02d}".format(y)+'-'+str(monthrange(int(this_year),y)[1]), inclusive=False)]
				#print(this_year+'-'+"{:02d}".format(y-1)+'-'+str(monthrange(int(this_year),y-1)[1]),this_year+'-'+"{:02d}".format(y)+'-'+str(monthrange(int(this_year),y)[1]))
				jul.append([x,len(temp_)])
			elif y == 8:
				month_range = monthrange(int(this_year), y)
				temp_ = clusters[x].loc[clusters[x]['date'].between(this_year+'-'+"{:02d}".format(y-1)+'-'+str(monthrange(int(this_year),y-1)[1]),this_year+'-'+"{:02d}".format(y)+'-'+str(monthrange(int(this_year),y)[1]), inclusive=False)]
				#print(this_year+'-'+"{:02d}".format(y-1)+'-'+str(monthrange(int(this_year),y-1)[1]),this_year+'-'+"{:02d}".format(y)+'-'+str(monthrange(int(this_year),y)[1]))
				aug.append([x,len(temp_)])
			elif y == 9:
				month_range = monthrange(int(this_year), y)
				temp_ = clusters[x].loc[clusters[x]['date'].between(this_year+'-'+"{:02d}".format(y-1)+'-'+str(monthrange(int(this_year),y-1)[1]),this_year+'-'+"{:02d}".format(y)+'-'+str(monthrange(int(this_year),y)[1]), inclusive=False)]
				#print(this_year+'-'+"{:02d}".format(y-1)+'-'+str(monthrange(int(this_year),y-1)[1]),this_year+'-'+"{:02d}".format(y)+'-'+str(monthrange(int(this_year),y)[1]))
				sep.append([x,len(temp_)])
			elif y == 10:
				month_range = monthrange(int(this_year), y)
				temp_ = clusters[x].loc[clusters[x]['date'].between(this_year+'-'+"{:02d}".format(y-1)+'-'+str(monthrange(int(this_year),y-1)[1]),this_year+'-'+"{:02d}".format(y)+'-'+str(monthrange(int(this_year),y)[1]), inclusive=False)]
				#print(this_year+'-'+"{:02d}".format(y-1)+'-'+str(monthrange(int(this_year),y-1)[1]),this_year+'-'+"{:02d}".format(y)+'-'+str(monthrange(int(this_year),y)[1]))
				oct_.append([x,len(temp_)])
			elif y == 11:
				month_range = monthrange(int(this_year), y)
				temp_ = clusters[x].loc[clusters[x]['date'].between(this_year+'-'+"{:02d}".format(y-1)+'-'+str(monthrange(int(this_year),y-1)[1]),this_year+'-'+"{:02d}".format(y)+'-'+str(monthrange(int(this_year),y)[1]), inclusive=False)]
				#print(this_year+'-'+"{:02d}".format(y-1)+'-'+str(monthrange(int(this_year),y-1)[1]),this_year+'-'+"{:02d}".format(y)+'-'+str(monthrange(int(this_year),y)[1]))
				nov.append([x,len(temp_)])
			else:
				month_range = monthrange(int(this_year), y)
				temp_ = clusters[x].loc[clusters[x]['date'].between(this_year+'-'+"{:02d}".format(y-1)+'-'+str(monthrange(int(this_year),y-1)[1]),this_year+'-'+"{:02d}".format(y)+'-'+str(monthrange(int(this_year),y)[1]), inclusive=False)]
				#print(this_year+'-'+"{:02d}".format(y-1)+'-'+str(monthrange(int(this_year),y-1)[1]),this_year+'-'+"{:02d}".format(y)+'-'+str(monthrange(int(this_year),y)[1]))
				dec_.append([x,len(temp_)])


	plt.figure(figsize=(20,10))

	e = 0
	xs, ys = [*zip(*jan)]
	plt.plot(xs, ys, label="January")

	e += sum (ys)

	xs, ys = [*zip(*feb)]
	plt.plot(xs, ys, label="February")
	e += sum (ys)
	xs, ys = [*zip(*mar)]
	plt.plot(xs, ys, label="March")
	e += sum (ys)
	xs, ys = [*zip(*apr)]
	plt.plot(xs, ys, label="April")
	e += sum (ys)
	xs, ys = [*zip(*may)]
	plt.plot(xs, ys, label="May")
	e += sum (ys)
	xs, ys = [*zip(*jun)]
	plt.plot(xs, ys, label="June")
	e += sum (ys)
	xs, ys = [*zip(*jul)]
	plt.plot(xs, ys, label="July")

	xs, ys = [*zip(*aug)]
	plt.plot(xs, ys, label="August")

	xs, ys = [*zip(*sep)]
	plt.plot(xs, ys, label="September")

	xs, ys = [*zip(*oct_)]
	plt.plot(xs, ys, label="October")

	xs, ys = [*zip(*nov)]
	plt.plot(xs, ys, label="November", color='#7c3759')

	xs, ys = [*zip(*dec_)]
	plt.plot(xs, ys, label="December", color='#311085')


	#plt.bar(x, y)
	plt.title("Number of Articles per Month")
	plt.xlabel('Cluster')
	plt.ylabel('Number of News Articles')

	tmp = []
	cl_nm_len = len(cluster_names)
	for a in range(0,cl_nm_len):
		tmp.append(cluster_names[str(a)])

	plt.xticks(np.arange(gm.kmeans.n_clusters), (tmp))
	plt.legend()

	plt.show()

def pca():
    import matplotlib.pyplot as plt
    from sklearn.decomposition import PCA
    #from sklearn.manifold import TSNE

    num_clusters = 10
    num_seeds = 10
    max_iterations = 300
    labels_color_map = {
        0: '#20b2aa', 1: '#ff7373', 2: '#ffe4e1', 3: '#005073', 4: '#4d0404',
        5: '#ccc0ba', 6: '#4700f9', 7: '#f6f900', 8: '#00f91d', 9: '#da8c49'
    }
    pca_num_components = 2
    tsne_num_components = 2
    
    labels = gm.kmeans.fit_predict(gm.X3)
    # print labels

    X = gm.X3.todense()

    # ----------------------------------------------------------------------------------------------------------------------

    reduced_data = PCA(n_components=pca_num_components, svd_solver='auto', whiten=True).fit_transform(X)
    # print reduced_data

    fig, ax = plt.subplots()
    for index, instance in enumerate(reduced_data):
        # print instance, index, labels[index]
        pca_comp_1, pca_comp_2 = reduced_data[index]
        color = labels_color_map[labels[index]]
        ax.scatter(pca_comp_1, pca_comp_2, c=color)
    plt.show()


    '''# t-SNE plot
    embeddings = TSNE(n_components=tsne_num_components)
    Y = embeddings.fit_transform(X)
    plt.scatter(Y[:, 0], Y[:, 1], cmap=plt.cm.get_cmap(name='plasma', lut=None))
    plt.show()
    '''

def tsne():
    from sklearn.decomposition import TruncatedSVD

    svd = TruncatedSVD(n_components=50, random_state=0)
    svd_tfidf = svd.fit_transform(gm.X3)
    
    from sklearn.manifold import TSNE
    fig, ax = plt.subplots(figsize = (10,8))
    kmeans_clustering = gm.kmeans
    idx = kmeans_clustering.fit_predict( gm.X3 )

    
    X = TSNE(n_components=2,perplexity=30, n_iter=1000, learning_rate=300 ).fit_transform( svd_tfidf )

    colors = np.array([x for x in 'bgrcmykbgrcmykbgrcmykbgrcmyk'])
    plt.scatter(X[:,0], X[:,1], c=colors[kmeans_clustering.labels_])
    plt.title('Model Scatterplot')
    plt.show()








