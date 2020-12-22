import sys
import random as r

print('词汇抽背程序，配合词汇登记程序使用')
print('V0.2')
print('author: 陈波文(ちん　はぶん)')


def main():
	db = read_lib()  # 从文件读取库
	db = get_tab(db)  # 从库中抽取一个tab
	txt = mode = ''
	while txt not in '12' or len(txt) != 1:  # 选择抽背方式
		txt = input('\n1.看平假名输入含义\n2.看含义输入平假名\n请输入序号：')
		if txt == '1':
			mode = 'kana2meaning'
		elif txt == '2':
			mode = 'meaning2kana'
	question(db, mode)


def read_lib():
	"""
	用于读取数据库的函数
	:return: dict 数据库字典
	"""
	with open('database2.txt', 'r', encoding='utf-8') as database:
		text = database.read()
	if text:
		return eval(text)
	else:
		print('数据库为空，无法抽背，程序结束')
		sys.exit()


def get_tab(db: dict):
	"""
	用于获取要抽背的单词库
	:param db: 全数据库
	:return: 相应的分库
	"""
	keys = list(db.keys())
	print('数据库现有以下tab')
	print('序号\t名称')
	for index, key in enumerate(keys):
		print(index, '\t', key)
	index = eval(input('请输入想使用的库的序号：'))
	return db[keys[index]]


def question(db: dict, mode: str):
	"""
	用于抽背的
	:param db:包含抽背内容的数据库，结构为：{'kana': ['汉字', '含义']}
	:param mode:
	:return:
	"""
	while 1:
		pool = list(db.keys())
		working = list()
		old = kana = None
		while pool or working:  # 抽一轮单词
			# 随时保持working池有5个单词
			while len(working) < 5 and pool:
				working.append(pool.pop(r.randint(0, len(pool)-1)))
			# 抽取问题
			kana = r.choice(working)
			while old == kana and len(working) > 1:  # 防止重复
				kana = r.choice(working)
			old = kana
			meaning = db[kana][1]
			# 显示问题
			print('ToDo：', len(working)+len(pool))
			if mode == 'kana2meaning':
				print(kana, end='')
				# 处理交互（是否将当前词汇留在词汇池里）
				txt = input('\t')
				if not txt or txt in meaning:  # 当答对或pass时，更新working列表
					working.remove(kana)
				print(db[kana][0], '(', db[kana][1], ')\n')
			else:
				print(meaning, end='')
				# 处理交互（是否将当前词汇留在词汇池里）
				txt = input('\t')
				if not txt or txt == kana or txt == db[kana][0]:  # 当答对或pass时，更新working列表
					working.remove(kana)
				if db[kana][0]:
					print(kana, '(', db[kana][0], ')\n')
				else:
					print(kana, '\n')


if __name__ == "__main__":
	main()
