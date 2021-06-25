# from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# from flask_login import UserMixin

# import json

# base = declarative_base()

# class Vms(base):
#     __tablename__ = "vms"

#     id = Column('id', Integer, primary_key=True)
#     architecture = Column('architecture', String)
#     config = Column('config', String)
#     created_at = Column('created_at', String)
#     devices = Column('devices', String)
#     ephemeral = Column('ephemeral', String)
#     expanded_config = Column('expanded_config', String)
#     expanded_devices = Column('expanded_devices', String)
#     name = Column('name', String)
#     description = Column('description', String)
#     profiles = Column('profiles', String)
#     status = Column('status', String)
#     last_used_at = Column('last_used_at', String)
#     location = Column('location', String)
#     types = Column('types', String)
#     status_code = Column('status_code', String)
#     stateful = Column('stateful', String)

#     def __init__(
#         self, 
#         architecture, 
#         config, 
#         created_at, 
#         devices,
#         ephemeral, 
#         expanded_config, 
#         expanded_devices, 
#         name,
#         description, 
#         profiles, 
#         status, 
#         last_used_at,
#         location, 
#         types,
#         status_code, 
#         stateful
#         ):
#         self.architecture = architecture
#         self.config = config
#         self.created_at = created_at
#         self.devices = devices
#         self.ephemeral = ephemeral
#         self.expanded_config = expanded_config
#         self.expanded_devices = expanded_devices
#         self.name = name
#         self.description = description
#         self.profiles = profiles
#         self.created_at = created_at
#         self.devices = devices
#         self.architecture = architecture
#         self.config = config
#         self.status = status
#         self.last_used_at = last_used_at
#         self.location = location
#         self.types = types
#         self.status_code = status_code
#         self.stateful = stateful

class Hypervisor:
    
    def __init__(self, system, node, release, version, machine, processor):
        self.system = system
        self.node = node
        self.release = release
        self.version = version
        self.machine = machine
        self.processor = processor


# class Users(UserMixin, base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True)
#     email = Column(String(100), unique=True)
#     password = Column(String(100))

# if __name__ == '__main__':
#     engine = create_engine('sqlite:///db.sqlite')
#     base.metadata.create_all(engine)