from warm_transfer_flask import db

class ActiveCall(db.Model):
    __tablename__ = 'active_calls'

    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.String, nullable=False)
    conference_id = db.Column(db.String, nullable=False)

    @classmethod
    def create(cls, agent_id, conference_id):
        existing_call = cls.query.filter_by(agent_id=agent_id).first()
        current_call = existing_call or cls(agent_id, conference_id)
        current_call.conference_id = conference_id
        db.session.add(current_call)
        db.session.commit()

    @classmethod
    def conference_id_for(cls, agent_id):
        return cls.query.filter_by(agent_id=agent_id).first().conference_id

    def __init__(self, agent_id, conference_id):
        self.agent_id = agent_id
        self.conference_id = conference_id
        
class NumberConfig(db.Model):
    __tablename__ = 'number_config'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String, nullable=False)
    sip = db.Column(db.String, nullable=False)
    extension = db.Column(db.String, nullable=False)

    @classmethod
    def create(cls, number, extension, sip):
        print number + sip + extension
        existing_number = cls.query.filter_by(number=number).first()
        print 'existing_number: ', existing_number and existing_number.number + existing_number.sip or 'none'
        current_number = existing_number or cls(number, extension, sip)
        current_number.sip = sip
        current_number.extension = extension
        current_number.number = number
        print 'current_number: ', current_number.number
        db.session.add(current_number)
        db.session.commit()

    @classmethod
    def extension_for(cls, number):
        return cls.query.filter_by(number=number).first().sip
    
    @classmethod
    def number_for(cls, extension, sip):
        print  sip + extension
        existing_number = cls.query.filter_by(extension=extension).first()
        return existing_number and existing_number.number or '+18637774494'

    def __init__(self, number, extension, sip):
        self.number = number
        self.sip = sip
        self.extension = extension
