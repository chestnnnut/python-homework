# -*- coding: utf-8 -*-
"""
微博词频分析
"""


#词频分析
# In[*] 
import re
import jieba
import zhon.hanzi
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from wordcloud import WordCloud
import jieba.posseg as pseg
from collections import Counter  

# In[*] 读取文件生成二维列表
data  =  []
with  open ("C:\\Users\\曾琳\\Desktop\\大二下作业\\python数据分析\\第一次作业-词频分析\\weibo.txt","r",  encoding='utf-8',errors = 'ignore') as  myfile:
    all_data = myfile.readlines()
    for  i in  range(len(all_data)):
        temp_list = []
        for element in all_data[i].split():
            temp_list.append(element)
        data.append(temp_list)
    
# In[*] 定义数据清洗函数
def clean(text):
    text = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:| |$)", " ", text)  # 去除正文中的@和回复/转发中的用户名
    text = re.sub(r"\[\S+\]", "", text)      # 去除表情符号
    text = re.sub(r"#\S+#", "", text)      # 保留话题内容
    URL_REGEX = re.compile(
        r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
        re.IGNORECASE)
    text = re.sub(URL_REGEX, "", text)       # 去除网址
    text = text.replace("转发微博", "")       # 去除无意义的词语
    text = re.sub(r"\s+", " ", text) # 合并空格
    text = re.sub(",+", ",", text)  # 合并逗号
    text = re.sub(" +", " ", text)  # 合并空格
    text = re.sub("[...|…|。。。]+", ".", text)  # 合并句号
    text = re.sub("-+", "--", text)  # 合并-
    text = re.sub("———+", "———", text)  # 合并-
    return text.strip()

# In[*]  获取初步的整体分词结果
comments=[]
for i in data:
    i[2]=clean(i[2])#评论数据清洗,并且只保留有效文本
    comments.append(i[2])
#print(comments)

jiebaword=[]
for line in comments:
    line = line.strip('\n')
    # 清除多余的空格
    line = "".join(line.split())
    # 分词
    ls = jieba.lcut(line)
    jiebaword.append(ls)
#print(jiebaword)
    
# In[*] 标点和停用词    
punc = zhon.hanzi.punctuation  #要去除的中文标点符号

def stopwordlist():
    stopwordlist=[]
    sws = [line.strip() for line in open('C:\\Users\\曾琳\\Desktop\\大二下作业\\python数据分析\\第一次作业-词频分析\\stopwords_list.txt','r',encoding='utf-8').readlines()]
    stopwordlist.extend(sws)
    return list(set(stopwordlist))
sw = stopwordlist()#导入停用词

# In[*] 统计词频 
counts= {}
for line in jiebaword:
    for i in line:
        if len(i)>1:        
            counts[i] = counts.get(i,0)+1

for p in punc:#去标点
    counts.pop(p,0)

for word in sw:  #去掉停用词
    counts.pop(word,0)

jiebaword_sorted_list = sorted(counts.items(),key=lambda x:x[1],reverse=True) #词频排序
#print(jiebaword_sorted_list[:20])

# In[*] 画整体词云
font = r'C:\\Windows\\Fonts\\msyh.ttc'#设置字体路径

img = Image.open(r'C:\\Users\\曾琳\\Desktop\\大二下作业\\python数据分析\\第一次作业-词频分析\\background.png') #打开图片
img_array = np.array(img) #将图片转换为数组
wc = WordCloud(
    background_color='white',
    width=1000,
    height=800,
    mask=img_array, #设置背景图片
    font_path=font
)
wc.generate_from_frequencies(counts)#绘制图片
plt.imshow(wc)
plt.axis('off')#隐藏坐标轴
plt.show()  #显示图片
wc.to_file(r'C:\\Users\\曾琳\\Desktop\\大二下作业\\python数据分析\\第一次作业-词频分析\\beautifulcloud.png')  #保存图片

# In[*] 按照词性重新分词
jiebaword_pseg=[]
for line in comments:
    line = line.strip('\n')
    # 清除多余的空格
    line = "".join(line.split())
    # 分词
    ls = pseg.cut(line)
    jiebaword_pseg.append(ls)

count_flag = {}
for line in jiebaword_pseg:
    for word ,flag in line:
        if flag not in count_flag.keys():  #如果没有flag键，就添加flag键，对应的值为一个空列表，每个键代表一种词性
            count_flag[flag] = []
        elif len(word)>1 and word not in sw:    #有对应的词性键，就将词加入到键对应的列表中，跳过长度为1和在停用词表中的词
            count_flag[flag].append(word)
#print(count_flag)
            
#统计各个词性的词频
flag_freq = {}
for flag in count_flag:
    flag_freq[flag]=len(count_flag[flag])
#print(flag_freq)

# In[*] 提取三个词性的词汇及频率，准备词云绘制
n = count_flag['n']
v = count_flag['v']
a = count_flag['a']
noun = Counter(n)
verb = Counter(v)
adj = Counter(a)
noun = dict(sorted(noun.items(), key=lambda x: x[1],reverse=True))
verb = dict(sorted(verb.items(), key=lambda x: x[1],reverse=True))
adj = dict(sorted(adj.items(), key=lambda x: x[1],reverse=True))
print("名词词频排序")
print(list(noun.items())[:20])
print("动词词频排序")
print(list(verb.items())[:20])
print("形容词词频排序")
print(list(adj.items())[:20])

# In[*] 分别绘制动词、名词、形容词词云
wc_n = WordCloud(background_color='white',width=1000,height=800,mask=img_array,font_path=font)
wc_n.generate_from_frequencies(noun)
plt.imshow(wc_n)
plt.axis('off')
wc_n.to_file(r'C:\\Users\\曾琳\\Desktop\\大二下作业\\python数据分析\\第一次作业-词频分析\\cloud_noun.png')
wc_v = WordCloud(background_color='white',width=1000,height=800,mask=img_array,font_path=font)
wc_v.generate_from_frequencies(verb)
plt.imshow(wc_v)
plt.axis('off')
wc_v.to_file(r'C:\\Users\\曾琳\\Desktop\\大二下作业\\python数据分析\\第一次作业-词频分析\\cloud_verb.png')
wc_a = WordCloud(background_color='white',width=1000,height=800,mask=img_array,font_path=font)
wc_a.generate_from_frequencies(adj)
plt.imshow(wc_a)
plt.axis('off')
wc_a.to_file(r'C:\\Users\\曾琳\\Desktop\\大二下作业\\python数据分析\\第一次作业-词频分析\\cloud_adj.png')
