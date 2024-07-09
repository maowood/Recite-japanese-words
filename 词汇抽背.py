import sys
import random as r

print('词汇抽背程序，配合词汇登记程序使用')
print('V0.3')
print('author: 陈波文(ちん　はぶん)')

db = dict()  # database2.txt文件里的全部内容结构为：db: dict = { tab1: { kana: [ han, cn ], kana2: .. }, tab2: .. }
tab = dict()  # 本次抽背使用的tab
tab_name = str()  # 本次使用的tab名
review_tab_name = '**review**'


def main():
	global db, tab
	db = read_lib()  # 从文件读取库
	tab = get_tab()  # 从库中抽取一个tab
	txt = mode = ''
	while txt not in '12' or len(txt) != 1:  # 选择抽背方式
		txt = input('\n1.看平假名输入含义\n2.看含义输入平假名\n请输入序号：')
		if txt == '1':
			mode = 'kana2meaning'
		elif txt == '2':
			mode = 'meaning2kana'
	question(mode)


def read_lib():
	"""
	用于读取数据库的函数
	:return: dict 数据库字典
	"""
	with open('./database2.txt', 'r', encoding='utf-8') as database:
		text = database.read()
	if text:
		return eval(text)
	else:
		print('数据库为空，无法抽背，程序结束')
		sys.exit()


def write_lib():
	"""
	用于写入数据库的函数
	:return: None
	"""
	global db
	with open('database2.txt', 'w', encoding='utf-8') as database:
		db_str = str(db)
		# 格式化字符串，以提高可读性
		db_str = db_str.replace('],', '],\n')
		db_str = db_str.replace('},', '},\n\n')
		db_str = db_str.replace('\': {', '\': \n{')
		database.write(db_str)


def get_tab():
	"""
	用于获取要抽背的单词库
	:return: 相应的分库
	"""
	global db, tab_name
	keys = list(db.keys())
	print('数据库现有以下tab')
	print('序号\t名称')
	for index, key in enumerate(keys):
		print(index, '\t', key)
	index = eval(input('请输入想使用的库的序号：'))
	tab_name = keys[index]
	return db[keys[index]]


def incorrect_ans(key: str, value: list):
	"""
	当回答错误时，将这个单词记录到tab:review_tab_name，并更新database2.txt
	:param key: 键值对的key
	:param value: 键值对的value
	:return: None
	"""
	db.setdefault(review_tab_name, dict())
	db[review_tab_name][key] = value
	write_lib()
	

def question(mode: str):
	"""
	用于抽背的
	:param mode:抽问模式
	:return:
	"""
	global tab
	while 1:
		pool = list(tab.keys())
		working = list()
		old = None  # 用于记录上一个词汇，仿重复
		while pool or working:  # 抽一轮单词
			
			# 随时保持working池有5个单词
			while len(working) < 5 and pool:
				working.append(pool.pop(r.randint(0, len(pool)-1)))
				
			# 抽取问题
			kana = r.choice(working)
			while old == kana and len(working) > 1:  # 防止重复
				kana = r.choice(working)
			old = kana
			
			# 显示问题
			print('ToDo：', len(working)+len(pool))
			if mode == 'kana2meaning':
				working = kana2meaning(working, kana)
			elif mode == 'meaning2kana':
				working = meaning2kana(working, kana)


def kana2meaning(working: list, kana: str):
	"""
	当模式是看假名输入含义时，用此方法处理交互
	:param working: question()中的working列表
	:param kana: 正在抽取的假名
	:return: working
	"""
	global tab
	print(kana, end='')
	txt = input('\t')

	# 显示答案
	print(tab[kana][0], '(', tab[kana][1], ')\n')

	# 处理交互
	if txt == 'x':  # 当输入'x'，结束程序
		sys.exit()
	elif not txt or txt in tab[kana][1]:  # 当答对或pass时，更新working列表
		working.remove(kana)
		if tab_name == review_tab_name:
			done_review(kana)
	else:  # 当答错时，记录答错的单词
		incorrect_ans(kana, tab[kana])
	return working


def meaning2kana(working: list, kana: str):
	"""
	当模式是看假名输入含义时，用此方法处理交互
	:param working: question()中的working列表
	:param kana: 正在抽取的假名
	:return: working
	"""
	print(tab[kana][1], end='')
	txt = input('\t')

	# 输出答案
	if tab[kana][0]:
		print(kana, '(', tab[kana][0], ')\n')
	else:
		print(kana, '\n')

	# 处理交互
	if txt == 'x':  # 当输入'x'，结束程序
		sys.exit()
	elif not txt or txt == kana or txt == tab[kana][0]:  # 当答对或pass时，更新working列表
		working.remove(kana)
		if tab_name == review_tab_name:
			done_review(kana)
	else:  # 当答错时，记录答错的单词
		incorrect_ans(kana, tab[kana])
	return working


def done_review(kana: str):
	"""
	当在使用review_tab_name时，若答对，则从review_tab_name中移去相应单词。当review_tab_name为空时，将其移去
	:param kana: 正在背的假名
	:return: None
	"""
	global db
	db[review_tab_name].pop(kana)
	# 当review tab为空时，移去该tab，并结束程序
	if not db[review_tab_name]:
		db.pop(review_tab_name)
		print("已完成复习，程序即将退出")
		write_lib()
		sys.exit()
	write_lib()


if __name__ == "__main__":
	main()
