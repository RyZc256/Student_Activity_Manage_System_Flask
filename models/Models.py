# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, String, text, Enum
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT
from sqlalchemy.orm import relationship
from application import db


class College(db.Model):
    __tablename__ = 'college'

    id = Column(BIGINT(20), primary_key=True)
    name = Column(String(255), nullable=False)


class DepartmentJob(db.Model):
    __tablename__ = 'department_job'

    id = Column(BIGINT(20), primary_key=True, comment='编号')
    name = Column(String(255), nullable=False, comment='职位')


class Role(db.Model):
    __tablename__ = 'role'

    id = Column(INTEGER(5), primary_key=True, comment='角色编号')
    name = Column(String(255), nullable=False, comment='角色名称')


class Classtable(db.Model):
    __tablename__ = 'classtable'

    id = Column(BIGINT(20), primary_key=True, comment='编号')
    college = Column(ForeignKey('college.id', onupdate='CASCADE'), nullable=False, index=True, comment='学院 外键')
    name = Column(String(50), nullable=False, comment='班级名称')
    administrator = Column(BIGINT(20), index=True, comment='负责人 外键')
    abbreviation = Column(String(25), comment='简称')

    college_ForeignKey = relationship('College')


class User(db.Model):
    __tablename__ = 'user'

    id = Column(BIGINT(20), primary_key=True, comment='用户名')
    openid = Column(String(255), unique=True, comment='微信openid')
    password = Column(String(255), nullable=False, comment='密码')
    role = Column(ForeignKey('role.id', onupdate='CASCADE'), nullable=False, index=True, server_default=text("'3'"), comment='账号权限')
    last_login = Column(DateTime, comment='最后登录时间')
    status = Column(INTEGER(2), nullable=False, server_default=text("'0'"), comment='账号状态（1为封禁）')

    role_ForeignKey = relationship('Role')


class Userinfo(db.Model):
    __tablename__ = 'userinfo'

    id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, comment='用户编号 外键 ')
    name = Column(String(15), nullable=False, comment='用户名称')
    tel = Column(String(15), nullable=False, unique=True, comment='用户电话')
    age = Column(INTEGER(3), nullable=False, comment='用户年龄')
    mail = Column(String(255), unique=True, comment='用户邮件')
    sex = Column(INTEGER(2), nullable=False, comment='用户性别')
    avatar = Column(String(255), comment='头像URL')
    class_id = Column(ForeignKey('classtable.id', onupdate='CASCADE'), index=True, comment='用户班级 外键')
    idcard = Column(String(20), nullable=False, unique=True, comment='身份证')
    address = Column(String(255), comment='家庭住址')
    join_time = Column(Date, comment='用户加入时间')

    class_ForeignKey = relationship('Classtable')


class Activity(db.Model):
    __tablename__ = 'activity'

    id = Column(BIGINT(20), primary_key=True, comment='活动编号')
    name = Column(String(255), nullable=False, comment='活动名称')
    detail = Column(LONGTEXT, comment='活动内容')
    regiser_time = Column(DateTime, nullable=False, comment='活动报名起始时间')
    cutoff_time = Column(DateTime, comment='活动报名结束时间')
    limit_number = Column(INTEGER(11), nullable=False, comment='活动人数限制')
    start_time = Column(DateTime, nullable=False, comment='活动开始时间')
    end_time = Column(DateTime, nullable=False, comment='活动结束时间')
    address = Column(String(255), comment='活动地址')
    administrator = Column(ForeignKey('userinfo.id', onupdate='CASCADE'), nullable=False, index=True,comment='活动负责老师')
    user = Column(ForeignKey('userinfo.id', ondelete='SET NULL', onupdate='CASCADE'), index=True,comment='活动负责学生')

    administrator_ForeignKey = relationship('Userinfo', primaryjoin='Activity.administrator == Userinfo.id')
    user_ForeignKey = relationship('Userinfo', primaryjoin='Activity.user == Userinfo.id')


class Department(db.Model):
    __tablename__ = 'department'

    id = Column(BIGINT(20), primary_key=True, comment='部门编号')
    name = Column(String(50), nullable=False, comment='部门名称')
    administrator = Column(ForeignKey('userinfo.id', ondelete='SET NULL', onupdate='CASCADE'), index=True, comment='部门管理员')

    administrator_ForeignKey = relationship('Userinfo')


class ActivityScore(db.Model):
    __tablename__ = 'activity_score'

    id = Column(BIGINT(20), primary_key=True, comment='评分ID')
    score = Column(Float, nullable=False, comment='得分')
    activity = Column(ForeignKey('activity.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, comment='活动ID')
    user = Column(ForeignKey('userinfo.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, comment='评分人')
    datetime = Column(DateTime, nullable=False, comment='评分时间')

    activity_ForeignKey = relationship('Activity')
    user_ForeignKey = relationship('Userinfo')


class DepartmentServe(db.Model):
    __tablename__ = 'department_serve'

    id = Column(BIGINT(20), primary_key=True, comment='记录编号')
    department = Column(ForeignKey('department.id', onupdate='CASCADE'), nullable=False, index=True, comment='部门')
    job = Column(ForeignKey('department_job.id', onupdate='CASCADE'), nullable=False, index=True, server_default=text("'5'"), comment='职位')
    user = Column(ForeignKey('userinfo.id', ondelete='CASCADE', onupdate='CASCADE'), index=True, comment='用户id')
    start_date = Column(Date, nullable=False, comment='任职开始时间')
    end_date = Column(Date, server_default=text("'0000-00-00'"))

    department_ForeignKey = relationship('Department')
    department_job_ForeignKey = relationship('DepartmentJob')
    user_ForeignKey = relationship('Userinfo')


class ActivityFileCollect(db.Model):
    __tablename__ = 'activity_file_collect'

    id = Column(BIGINT(20), primary_key=True)
    activity = Column(ForeignKey('activity.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, comment='关联活动')
    start_time = Column(DateTime, nullable=False, comment='开始收集时间')
    end_time = Column(DateTime, comment='结束时间')
    view = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='0 不开放 1开放')

    activity_ForeignKey = relationship('Activity')


class ActivityRegiserRecord(db.Model):
    __tablename__ = 'activity_regiser_record'

    id = Column(BIGINT(20), primary_key=True, comment='报名记录编号')
    activity = Column(ForeignKey('activity.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, comment='活动编号')
    user = Column(ForeignKey('userinfo.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, comment='用户编号')
    datetime = Column(DateTime, nullable=False, comment='报名时间')
    status = Column(INTEGER(2), nullable=False, server_default=text("'0'"), comment='状态 0 不可用 1 可用')

    activity1 = relationship('Activity')
    userinfo = relationship('Userinfo')


class ActivitySignCode(db.Model):
    __tablename__ = 'activity_sign_code'

    id = Column(BIGINT(20), primary_key=True, comment='签到码编码')
    activity = Column(ForeignKey('activity.id', onupdate='CASCADE'), nullable=False, index=True, comment='签到码所属活动')
    status = Column(INTEGER(2), nullable=False, server_default=text("'1'"), comment='签到码状态 0 不可用 1 可用')
    code = Column(String(255), nullable=False, comment='签到码')
    end_time = Column(DateTime, nullable=False, comment='签到码结束时间')

    activity_ForeignKey = relationship('Activity')


class ActivitySignRecord(db.Model):
    __tablename__ = 'activity_sign_record'

    id = Column(BIGINT(20), primary_key=True, comment='签到记录编号 ')
    activity = Column(ForeignKey('activity.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, comment='活动编号')
    user = Column(ForeignKey('userinfo.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, comment='用户编号')
    datetime = Column(DateTime, nullable=False, comment='签到时间')
    code = Column(String(255), nullable=False, comment='使用签到码')
    position = Column(String(255), comment='签到位置')

    activity_ForeignKey = relationship('Activity')
    user_ForeignKey = relationship('Userinfo')


class ActivityFileRecord(db.Model):
    __tablename__ = 'activity_file_record'

    id = Column(BIGINT(20), primary_key=True, comment='文件编号')
    collect = Column(ForeignKey('activity_file_collect.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, comment='所属活动')
    path = Column(String(255), nullable=False, comment='文件路径')
    user = Column(ForeignKey('userinfo.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, comment='上传人')
    upload_time = Column(DateTime, nullable=False, comment='上传时间')

    file_collect_ForeignKey = relationship('ActivityFileCollect')
    user_ForeignKey = relationship('Userinfo')


class ActivityMedia(db.Model):
    __tablename__ = 'activity_media'

    id = Column(BIGINT(20), primary_key=True)
    activity = Column(ForeignKey('activity.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, comment='关联活动')
    url = Column(String(255), comment='图片URL')
    type = Column(Enum('image', 'video', 'doc'), nullable=False, comment='文件类型')

    activity1 = relationship('Activity')