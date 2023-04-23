from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 內部員工清單
employees = [
    {
        'id': 1,
        'name': '王小明'
    },
    {
        'id': 2,
        'name': '賀阿庭'
    },
    {
        'id': 3,
        'name': '蔡阿恆'
    }
]

# 已開團的清單，每個團購會有一個唯一的 ID，內容包括開團的描述、人數、到達日期、團主等等。
groups = [
    {
        'id': 1,
        'description': '團購產品1',
        'leader': '王小明',
        'date': '2023-04-30',
        'capacity': 10,
        'participants': []
    },
    {
        'id': 2,
        'description': '團購產品2',
        'leader': 'Alice',
        'date': '2023-05-05',
        'capacity': 5,
        'participants': []
    }
]

# 每個產品的清單，包括產品名稱、價格等等。
products = [
    {
        'id': 1,
        'name': '特斯拉',
        'price': 100
    },
    {
        'id': 2,
        'name': '生鮮雞蛋',
        'price': 200
    },
    {
        'id': 3,
        'name': '高爾夫球',
        'price': 300
    }
]

# 路由：首頁
@app.route('/')
def home():
    return render_template('home.html', groups=groups)

# 路由：開團
@app.route('/create-group', methods=['GET', 'POST'])
def create_group():
    if request.method == 'POST':
        # 取得表單提交的資料
        description = request.form['description']
        date = request.form['date']
        capacity = int(request.form['capacity'])
        leader_id = int(request.form['leader'])

        # 創建新的團購群組
        group_id = len(groups) + 1
        leader_name = [e['name'] for e in employees if e['id'] == leader_id][0]
        new_group = {
            'id': group_id,
            'description': description,
            'leader': leader_name,
            'date': date,
            'capacity': capacity,
            'participants': []
        }
        groups.append(new_group)

        return redirect(url_for('group_detail', group_id=group_id))
    else:
        return render_template('create-group.html', employees=employees)

# 路由：團購詳情
@app.route('/group/<int:group_id>')
def group_detail(group_id):
    group = [g for g in groups if g['id'] == group_id][0]
    participants = group['participants']
    available_products = [p for p in products if p not in participants]
    return render