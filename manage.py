# coding:utf-8
from flask import Flask,render_template
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from ihome import create_app,db




app = create_app("DevelopmentConfig")

# 创建管理工具对象
manager = Manager(app)
Migrate(app,db)
manager.add_command("app",MigrateCommand)









if __name__=="__main__":
    manager.run()