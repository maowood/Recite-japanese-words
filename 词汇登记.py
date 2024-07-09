print('数据库写入程序')
print('V0.3')
print('author: 陈波文(ちん　はぶん)')
# 读取文件
try:
	with open('database2.txt', 'r', encoding='utf-8') as database:
		text = database.read()
except FileNotFoundError:
	with open('database2.txt', 'a+', encoding='utf-8') as database:
		text = ''
if text:
	db: dict = eval(text)
else:
	db = dict()
# 选择或创建单词库
lib_name = input('请输入单词库名称：')
if lib_name not in db:
	db[lib_name] = dict()
# 记录单词
temp_db = dict()
while 1:
	jp = input('请输入日语：')
	if not jp:  # 输入空后可以继续输入汉语含义
		break
	han = input('请输入汉字：')
	if han == 'x':  # 输入错误时，可以通过输入x来跳过本轮
		print('已跳过本单词')
		continue
	elif jp:  # 将数据写入内存
		temp_db[jp] = [han, '']
		print('已记录', jp, '：[', han, ',""]')
# 记录汉语含义
print('\n请输入汉语含义')
for jp in temp_db.keys():
	cn = input('%s: ' % jp)
	while not cn:  # 以防漏输入
		cn = input('请输入%s: ' % jp)
	temp_db[jp][1] = cn
# 格式化并写入数据库
db[lib_name].update(temp_db)

with open('database2.txt', 'w', encoding='utf-8') as database:
	db_str = str(db)
	# 格式化字符串，以提高可读性
	db_str = db_str.replace('],', '],\n')
	db_str = db_str.replace('},', '},\n\n')
	db_str = db_str.replace('\': {', '\': \n{')
	database.write(db_str)
	print('文件写入已完成')
