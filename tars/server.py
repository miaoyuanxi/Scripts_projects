# -*- coding: utf-8 -*-
from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all()
from flask import Flask, request, jsonify, Response
import os
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
StageCfg = {
    "max":{
        "before": ['RBBackupPy', 'RBinitLog', 'send_all_data', 'RBnodeClean',
                   'RBprePy', 'RBmakeDir', 'RBcopyTempFile', 'readPyCfg', 'readRenderCfg',
                   'netPath', 'copyBlack', 'CheckDisk', 'RBhanFile', 'RBrenderConfig',
                   'RBwriteConsumeTxt', 'resourceMonitor'],
        "core": ['RBrender'],
        "after": ['RBconvertSmallPic', 'RBhanResult', 'RBpostPy'],
    }
}


basedir= os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = r'mysql+pymysql://eiboe:eiboe@127.0.0.1:3306/data_ser'
# app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///'+ os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Task_info(db.Model):
    __tablename__ = 'task_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String(100))
    task_id = db.Column(db.Integer)
    job_id = db.Column(db.Integer)
    soft = db.Column(db.String(100))
    ip = db.Column(db.String(100))
    platform = db.Column(db.String(100))
    system = db.Column(db.String(100))
    random_num = db.Column(db.Integer)
    phase = db.Column(db.String(100))
class Task_exetime(db.Model):
    __tablename__ = 'task_exetime'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String(100))
    task_id = db.Column(db.Integer)
    job_id = db.Column(db.Integer)
    action = db.Column(db.String(200))
    start_time = db.Column(db.String(200))
    end_time = db.Column(db.String(200))
    total_time = db.Column(db.String(200))
    random_num = db.Column(db.Integer)
    phase = db.Column(db.String(100))

db.drop_all()


db.create_all()


@app.route('/taskinfo', methods=['POST'])
def taskinfo():
    if request.method == 'POST':
        # POST:
        # request.form获得所有post参数放在一个类似dict类中,to_dict()是字典化
        # 单个参数可以通过request.form.to_dict().get("xxx","")获得
        # ----------------------------------------------------
        # GET:
        # request.args获得所有get参数放在一个类似dict类中,to_dict()是字典化
        # 单个参数可以通过request.args.to_dict().get('xxx',"")获得
        date = request.form.to_dict().get("date")
        task_id = request.form.to_dict().get("task_id")
        job_id = request.form.to_dict().get("job_id")
        soft = request.form.to_dict().get("soft")
        ip = request.form.to_dict().get("ip")
        platform = request.form.to_dict().get("platform")
        system = request.form.to_dict().get("system")
        random_num = request.form.to_dict().get("random_num")
        phase = request.form.to_dict().get("phase")
        db.session.add(Task_info(date=date, task_id=task_id, job_id=job_id, soft=soft, ip=ip, platform=platform, system=system, random_num=random_num, phase=phase))
        db.session.commit()

        return 'OK'

@app.route('/exetime', methods=['POST'])
def exetime():
    if request.method == 'POST':
        task_id = request.form.to_dict().get("task_id")
        job_id = request.form.to_dict().get("job_id")
        date = request.form.to_dict().get("date")
        action = request.form.to_dict().get("action")
        start_time = request.form.to_dict().get("start_time")
        end_time = request.form.to_dict().get("end_time")
        total_time = request.form.to_dict().get("total_time")
        random_num = request.form.to_dict().get("random_num")
        phase = request.form.to_dict().get("phase")
        db.session.add(Task_exetime(task_id=task_id, job_id=job_id, date=date, action=action, start_time=start_time, end_time=end_time, total_time=total_time, random_num=random_num, phase=phase))
        db.session.commit()
        return 'OK'

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
    #app.run(host='0.0.0.0', debug=True)
