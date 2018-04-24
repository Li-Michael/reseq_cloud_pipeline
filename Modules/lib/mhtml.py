# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
class table_html(object):
	def __init__(self,listhead,table_title=""):
		#self.head = """<table frame="hsides" border="1" cellpadding="2" align="left" cellspacing="0">\n"""+"""<caption align="top">%s</caption>"""%table_title
		self.head = """<table frame="hsides" border="1" cellpadding="2" cellspacing="0">\n"""+"""<caption align="top">%s</caption>"""%table_title
		self.end = """</table>\n"""
		self.h_head = """<tr>"""
		self.h_end = """</tr>"""
		self.v_head = """<td style='text-align:center'>"""
		self.v_end = """</td>"""
		self.button = ''
		self.listhead = listhead[:]
		self.length = len(self.listhead)
		self.content = []
		strcontent = "<tr>"
		for i in xrange(self.length):
			strcontent += "<th style='text-align:center'>"+str(listhead[i])+"</th>"
		strcontent += "</tr>"
		self.content.append(strcontent)
	def add_row(self,content, number = 1):
		assert len(content) == self.length
		strcontent = "<tr>"
		for i in xrange(self.length):
			strcontent += "<td style='text-align:center' rowspan = {}><pre>".format(number)+str(content[i])+"</pre></td>"
		strcontent += "</tr>"
		self.content.append(strcontent)
	def add_noprerow(self,content):
		assert len(content) == self.length
		strcontent = "<tr>"
		for i in xrange(self.length):
			strcontent += "<td style='text-align:center'>"+str(content[i])+"</td>"
		strcontent += "</tr>"
		self.content.append(strcontent)
	def __str__(self):
		return "\n".join([self.head,"\n".join(self.content),self.end])

def return_top():
	top_str = u"""
	<script>
	var displayed="<nobr><b>[Top]</b></nobr>"
	var logolink='javascript:window.scrollTo(0,0)'
	var ns4=document.layers
	var ie4=document.all
	var ns6=document.getElementById&&!document.all

	function regenerate(){
	window.location.reload()
	}
	function regenerate2(){
	if (ns4)
	setTimeout("window.onresize=regenerate",400)
	}

	if (ie4||ns6)
	document.write('<span id="logo" style="position:absolute;top:-300;z-index:100">'+displayed+'</span>')

	function createtext(){ //function for NS4
	staticimage=new Layer(5)
	staticimage.left=-300
	staticimage.document.write('<a href="'+logolink+'">'+displayed+'</a>')
	staticimage.document.close()
	staticimage.visibility="show"
	regenerate2()
	staticitns()
	}

	function staticit(){ //function for IE4/ NS6
	var w2=ns6? pageXOffset+w : document.body.scrollLeft+w
	var h2=ns6? pageYOffset+h : document.body.scrollTop+h
	crosslogo.style.left=w2
	crosslogo.style.top=h2
	}

	function staticit2(){ //function for NS4
	staticimage.left=pageXOffset+window.innerWidth-staticimage.document.width-28
	staticimage.top=pageYOffset+window.innerHeight-staticimage.document.height-10
	}

	function inserttext(){ //function for IE4/ NS6
	if (ie4)
	crosslogo=document.all.logo
	else if (ns6)
	crosslogo=document.getElementById("logo")
	crosslogo.innerHTML='<a href="'+logolink+'">'+displayed+'</a>'
	w=ns6? window.innerWidth-crosslogo.offsetWidth-20 : document.body.clientWidth-crosslogo.offsetWidth-10
	h=ns6? window.innerHeight-crosslogo.offsetHeight-30 : document.body.clientHeight-crosslogo.offsetHeight-10
	crosslogo.style.left=w
	crosslogo.style.top=h
	if (ie4)
	window.onscroll=staticit
	else if (ns6)
	startstatic=setInterval("staticit()",100)
	}

	if (ie4||ns6){
	window.onload=inserttext
	window.onresize=new Function("window.location.reload()")
	}
	else if (ns4)
	window.onload=createtext

	function staticitns(){ //function for NS4
	startstatic=setInterval("staticit2()",90)
	}

	</script>
	"""
	return top_str
class simple_main(object):
	def __init__(self,title="Result report",css="CSS"):
		#start = """<html><body><h1>KEGG Pathway Enrichment Analysis</h1><hr />"""
		self.start = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>%s</title>\n
<link href="%s/report.css" rel="stylesheet" type="text/css"><link rel="stylesheet" type="text/css" href="%s/base_new.css">
</head>
<body>"""%(title,css, css) ###also can add 
		self.start1 = """ <html> <head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>%s</title><link href="%s/report.css" rel="stylesheet" type="text/css"></head><body><link rel="stylesheet" type="text/css" href="%s/base_new.css">"""%(title,css,css)
#<link href="Files/Pages/css/report.css" rel="stylesheet" type="text/css">
#<script language="javascript" src="Files/Pages/js/jquery.js"></script>
#<script language="javascript" src="Files/Pages/js/report.js"></script>
		self.end = """</body></html>"""
		self.content = ""
		self.cato = ""
		self.title = ""
		self.heads = []
		self.id = 1
		self.example_id = 0
		self.headcolors = {1:"#6600CC",
				2:"#6600CC",
				3:"green",
				4:"#996600",
				5:"#996600",
				6:"#996600",
				}
	def add_head(self,content,headlevel=1, loc='left', color='black'):
		self.content += "<div align='%s'><h%d><font color=%s face='Times'>%s</font></h%d></div>\n"%(loc, headlevel,color,content,headlevel)
	
	def add_head_color(self, content,  headlevel=1):
		self.content += "<h%d style='color:%s'><a name='%d'></a>%s</h%d><p style='line-height:0.3em'><br/></p>\n"%(headlevel,self.headcolors[headlevel],self.id ,content,headlevel)
		if 0 < headlevel < 4:
			self.heads.append([content,self.id,headlevel])
		self.id += 1
	
	def add_head_line(self, color='teal', width='100%', size=10):
		self.content += "<hr color='%s' width='%s' style='height:%dpx'/>"%(color, width, size)
	
	def add_href(self, content, hrefname):
		self.content += """<a href='%s'>%s</a>"""%(content, hrefname)
	
	def add_image(self, content, width=60, height=100, svg=1):
		if svg:
			self.content += """<img src='%s' width = "%d%%" height="%d%%"><a href='%s'>SVG矢量版本</a>"""%(content[0], width, height, content[-1])
		else:
			self.content += """<img src='%s' width = "%d%%" height="%d%%">"""%(content[0], width, height)

	def __add_head_bold_color(self,content,color = 'blue', headlevel=1):
		self.title += "<h%d><span style='font-weight:bold;'><font color=%s>%s</font></span></h%d>\n"%(headlevel,color,content,headlevel)
		
	def __add_frame_open(self, border = 2, style = "dashed", color = "green", width = 400, height = 650, margin = 10):
		self.cato += "<style>.bor{border:%dpx %s %s; width:%dpx; height:%dpx; margin-top:%dpx}"%(border, style, color, width, height, margin) + "</style>" + "<body>" + "<ul class=bor>"
	
	def __add_frame_content(self, content, char_size, char, wordsize, wordcolor, typeface, level,tmpid):
		if level == 0:
			self.cato += "<div align=left>" + "<span style='font-weight:bold;'>" + "<font style='font-size:%dpx;color:black'>"%(char_size) + "&%s;"%char + "</font>" + "</span>" + "<font style='font-size:%dpx; color: %s ;face:%s'>"%(wordsize, wordcolor, typeface) + "<a href='#%d' style='text-decoration:none'>%s</a><br/>"%(tmpid,content) + "</font>" + "</div>"
		elif level == 1:
			self.cato += "&nbsp;" + "&nbsp;" + "<span style='font-weight:bold;'>" + "<font size=%d color='black'>"%(char_size) + "&%s;"%char + "</font>" + "</span>" + "<font style='font-size:%dpx; color: %s; face:%s'>"%(wordsize, wordcolor, typeface) + "<a href='#%d' style='text-decoration:none'>%s</a>"%(tmpid,content) + "</font><br />"
	
	def __add_frame_close(self):
		self.cato += "</ul>" + "</body>" + "<hr color='teal' width='100%' style='height:20px'/>"
	
	def add_frame(self, content, border =1, width = 300, height = 60, marginTop = 10, dashColor = '#F00'):
		tmpStr = """<style>.bor{border:%ipx dashed %s;width:%ipx;height:%ipx;margin-top:%ipx}span{display:block}\
					</style>"""%(border,dashColor,width,height,marginTop)
		self.content += (tmpStr + "<div class=bor>{}</div>".format(content))
	
	def add_content(self,content, fontColor = 'black'):
		self.content += "<p>"+"""<font color={}>""".format(fontColor)+content+"</font>"+"</p>\n"
	
	def add_color_content(self, content, color='blue'):
		self.content += "<font color=%s>" + content + "</font>"

	def add_content_retract(self, content, level = 1, dis=0.2):
		if level==1:
			self.content += "&nbsp&nbsp"+content+"<br />\n"
		else:
			self.content += "&nbsp&nbsp"+content+"""<p style="line-height:%fem"><br/></p>"""%dis

	def add_content_span(self, content, dis=0.4):
		self.content += content + """<p style="line-height:%fem"><br/></p>"""%dis
	
	def add_checkbox(self, CheckBox = None, autoCheck = None, numCol = 3, ret = 0, spaceNum = 3, loc = 'center'):
		'''checkBox = {mainName: [], } or checkBox = []'''
		if not CheckBox: return None
		tmpContent = ''
		if isinstance(CheckBox, dict):
			for keyName in CheckBox:
				self.content += "<span style='font-weight:bold;'>"  + keyName + "</span><br />"
				for index, value in enumerate(CheckBox[keyName]):
					try:
						boolRes = value in autoCheck
						if boolRes:
							check = "checked"
						else: check = ""
					except:
						check = ""
					if (index + 1)%numCol is 0:
						tmpStr = """<input type="checkbox" name="q[]" id="q{}" {}/>
									<label for="q{}">{}</label></p>""".format(index, check, index, value)
					else:
						tmpStr = """<input type="checkbox" name="q[]" id="q{}" {}/>
									<label for="q{}">{}</label>{}""".format(index, check, index, value, '&nbsp'*spaceNum)
					if ret is 0:
						self.content += "<div align={}>".format(loc) + tmpStr
					else:
						tmpContent += tmpStr
				if ret:
					self.content += "<div align={}>".format(loc)
					self.content += tmpContent
					tmpContent = ''
				else:
					self.content += """</div>"""
		elif isinstance(CheckBox, list):
			for index, value in enumerate(CheckBox):
				try:
					boolRes = value in autoCheck
					if boolRes:
						check = "checked"
					else: check = ''
				except:
					check = ""
				if (index + 1)%numCol is 0:
					tmpStr = """<input type="checkbox" name="q[]" id="q{}" {}/>
								<label for="q{}">{}</label></p>""".format(index, check, index, value)
				else:
					tmpStr = """<input type="checkbox" name="q[]" id="q{}" {}/>
								<label for="q{}">{}</label>{}""".format(index, check, index, value, '&nbsp'*spaceNum)
				if ret is 0:
					self.content += "<div align={}>".format(loc) + tmpStr
				else:
					tmpContent += tmpStr
			if ret:
				self.content += """<div align={}>""".format(loc) + tmpContent + '</div>'
			else:
				self.content += """</div>"""
	
	def add_listType(self, content, fontSize = 3, fontColor = 'black', \
							numCol = 3, numSpace1 = 2, numSpace2 = 3, style = '&bull;', loc = 'center', styleSize = 10, styleColor = 'black'):
		if not content: return None
		tmpStyle = """<font size={} color={}>""".format(styleSize, styleColor)
		tmpFont = """<font size={} color={}>""".format(fontSize, fontColor)
		self.content += '<div align={}>'.format(loc)
		for index, value in enumerate(content):
			if (index + 1)%numCol is 0:
				self.content += tmpStyle + style + "</font>" + "&nbsp" * numSpace1 + tmpFont + str(value) + "</font>"\
								+ "</div></p>"
				self.content += '<div align={}>'.format(loc)
			else:
				self.content += tmpStyle + style + "</font>" + "&nbsp" * numSpace1 + tmpFont + str(value) + "</font>"\
								+ "&nbsp" * numSpace2
		if (index + 1)%numCol <> 0:
			self.content += "</div></p>"

	def add_locate(self, content, loc = 'center'):
		self.content += """<div align=%s>%s</div>"""%(loc, content)
	
	def add_button(self, content, bgcolor = '#CCCCCC', fontcolor="blue"):
		self.button = """<button type='button' style='background:%s'><font color='%s'><span style='font-weight:bold;'>%s</span></font></button>"""%(bgcolor, fontcolor, content)	
		return(self.button)
	def add_abrest_open(self):
		self.content += """<table><tr>"""
	def add_abrest_content(self, content):
		self.content += """<td><div align='center'>%s</div></td>"""%content
	def add_abrest_close(self):
		self.content += """</tr></table>"""
	def add_reference(self, content, size=3, flag=0, dis=0.2):
		if flag==0:
			self.content += """&nbsp&nbsp<font size='%dpx' face='Times'>%s</font><br />"""%(size, content)
		else:
			self.content += """&nbsp&nbsp<font size='%dpx' face='Times'>%s</font><p style="line-height:%fem"><br/></p>"""%(size, content, dis)
	def add_abrest(self, listcontent, listdiscription):
		if listdiscription:
			for index , i in enumerate(listcontent):
				if index is 0:
					self.content += """<table><tr>""" + """<td><div align='center'>%s<br />%s</div></td>"""%(listcontent[index], listdiscription[index])
				elif index is len(listcontent) - 1:
					self.content += """<td><div align='center'>%s<br />%s</div></td>"""%(listcontent[index], listdiscription[index]) + "</tr></table>"
				else:
					self.content += """<td><div align='center'>%s<br />%s</div></td>"""%(listcontent[index], listdiscription[index])
		else:
			for i , index in enumerate(listcontent):
				if index is 0:
					self.content += """<table><tr>""" + """<td><div align='center'>%s</div></td>"""%(listcontent[index])
				elif index is len(listcontent) - 1:
					self.content += """<td><div align='center'>%s</div></td>"""%(listcontent[index]) + "</tr></table>"
				else:
					self.content += """<td><div align='center'>%s</div></td>"""%(listcontent[index])
			
	def add_genebang_title(self, title="重测序生物信息分析结题报告", site="left",pict="<img src='./HELP/Genebang/Genebang.png' width='20%%' />",nopict=0):
		if not nopict:
			self.title += "<div align=%s>"%site + pict + "</div>"
		self.__add_head_bold_color("<div align='center'>%s</div><br/>"%title, color = 'brown', headlevel = 1)
		self.title += "<hr color='%s' width='%s' style='height:%dpx'/> \n"%('brown', '100%', 2)
	
	def add_genebang(self, pict="<img src='./HELP/Genebang/Genebang.png' width='20%%' />", site='left'):
		self.content += "<div align=%s>"%site + pict + "</div>"
		
	def add_bold_color_content(self, content, color = 'blue'):
		self.content += "<span style='font-weight:bold;'>" + "<font color=%s>"%color + content + "</font>" + "</span>"

	def add_bold(self, content):
		self.content += "<span style='font-weight:bold;'>"  + content + "</span><br />"

	def add_precontent(self,content, fontColor='black'):
		self.content += "<p><pre>"+"""<font color={}>""".format(fontColor)+content+"</font>"+"</pre></p>\n"
	
	def add_line(self):
		self.content += "<hr />\n"
	
	def add_back1(self,content="返回上一页"):
		self.content += """<input type="button" name="Submit" onclick="javascript:history.back(-1);" value="返回上一页">\n"""
		#self.content += """<a href="<a href="javascript :history.back(-1)">返回上一页</a>\n"""
	
	def add_enter(self):
		self.content += "<br />\n"
	
	def add_slider_content(self, content, directory='./'):
		import os
		foreground = ''; list_content=[]
		file_names = os.listdir(directory); flag = 0
		for index, value in enumerate(file_names):
			tmp_path = directory + '/' + value + '/' + content
			if os.path.isfile(path):
				if flag is 0:
					foreground = path
					flag += 1
				else:
					list_content.append(path)
			else:
				pass
		return foreground, file_names	
	
	def select_dir(self, filename, statdir='./'):
		import os
		file_names = os.listdir(statdir)
		for line in file_names:
			if os.path.isfile(statdir + '/' + line + '/' + filename):
				statdir = statdir + '/' + line + '/'
				break
			elif os.path.isdir(statdir + '/' + line + '/' + filename):
				statdir = statdir + '/' + line + '/'
				break
		return statdir, line

	def add_slider(self, foreground,content):
		if content:
			length = len(content)
			self.content += """<p class="center"><div class="albumSlider"><div class="fullview"><img src=%s /></div><div class="slider"><div class="button movebackward" title="向上滚动"></div><div class="imglistwrap"><ul class="imglist">"""%foreground
			for i in xrange(length):
				self.content += """<li><a href=%s ><img src=%s /></a></li>"""%(content[i], content[i])
			self.content += """</ul></div><div class="button moveforward" title="向下滚动"></div></div></p>"""
	
	def __makecato(self):
		for tmphead,tmpid,headlevel in self.heads:
			if headlevel == 1:
				self.__add_frame_content(tmphead,20,"diams",24,'blue','宋体',0,tmpid)
			elif headlevel == 2:
				self.__add_frame_content(tmphead,20,"diams",20,'blue','宋体',0,tmpid)
			elif headlevel == 3:
				self.__add_frame_content(tmphead,4,"loz",17,'blue','宋体',1,tmpid)
			else:
				pass

	def __str__(self):
		if self.content == "":
			sys.stderr.write("[ERROR] html page has no content!\n")
			return None
		return "\n".join([self.start,self.content,self.end])
	
	
	def str_top(self,height=650, width=400,nocato=0):
		top_str = return_top()
		if self.content == "":
			sys.stderr.write("[ERROR] html page has no content!\n")
			return None
		if not nocato:
			self.__add_frame_open(height=height, width=width)
			self.__makecato()
			self.__add_frame_close()
		return "\n".join([self.start1,top_str,self.title,self.cato,self.content,self.end])

def get_sampleinfo(sampleinfo, number = 1):
	f = file(sampleinfo,"r")
	header = ["#","Samplename","Filename","SN","Category","Category name"]
	for line in f:
		if line.startswith("##"):continue
		if line.startswith("#"):
			header = ["#",] + line.rstrip("\n")[1:].split("\t")
			break
	f.seek(0)
	table = table_html(header,"Table: sample information list")
	idx = 1
	samplename = []
	files = []
	for line in f:
		if line.startswith("##"):continue
		if line.startswith("#"):
			header = ["#",] + line.rstrip("\n")[1:].split("\t")
			continue
		arr = line.rstrip("\n").split()
		sn = arr[0]
		files.append(arr[1].split(","))
		table.add_row([str(idx),"""<a href="#%s">%s</a>"""%(sn,sn)] + arr[1:], number = number)
		idx += 1
		samplename.append(sn)
	return str(table),samplename,files

def xls2table(fxls,title=None,header=None, rowNumber = 1000, merge_number = 1):
	f = file(fxls,"r")
	if header == None:
		header = "";
	if not title:
		title = "";
	rowNumber = int(rowNumber)
	for index, line in enumerate(f):
		if line.startswith("##"):
			title = "Table: "+line[2:].rstrip()
			continue
		elif line.startswith("#"):
			header = line.rstrip("\n").split("\t")
		else:break
	f.seek(0)
	table = table_html(header,title)
	note = ""; flag = 0
	while 1:
		line = f.readline()
		if not line: break
		if line.startswith("#"):continue
		if line.startswith("Note:"):
			note = line+f.read()
			break
		
		table.add_row(line.rstrip("\n").split("\t"), number = merge_number)
		if flag > rowNumber - 1: break
		flag += 1
	f.close()
	return str(table),note
if __name__  == "__main__":
	print get_sampleinfo(sys.argv[1])
