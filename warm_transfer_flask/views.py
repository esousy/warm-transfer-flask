from flask import render_template, jsonify, request, url_for
from . import token
from . import call
from . import twiml_generator
from .models import ActiveCall, NumberConfig
AGENT_WAIT_URL = 'http://twimlets.com/holdmusic?Bucket=com.twilio.music.classical'


def routes(app):
    app.route('/')(root)
    app.route('/conference/connect/client/<agent_id>', methods=['POST'])(connect_client)
    app.route('/<agent_id>/token', methods=['POST'])(generate_token)
    app.route('/conference/<agent_id>/call', methods=['POST'])(call_agent)
    app.route('/conference/wait', methods=['POST'])(wait)
    app.route('/conference/<conference_id>/connect/<agent_id>', methods=['POST'])(connect_agent)


def root():
    return render_template('index.html')


def connect_client(agent_id):
    dict = request.form
    for key in dict:
        print 'form key ', key, ' = ', dict[key]
    conference_id = request.form['CallSid']
    from_ = request.form['From']
    agent_sip = request.form['To']
    sip_user = 'sip:' + agent_id
    print 'sip_user: ', sip_user
    sip_numbers = agent_id.split('@')
    connect_agent_url = url_for('connect_agent', agent_id='agent1',
                                conference_id=conference_id, _external=True)
    call.call_agent(from_, sip_user, connect_agent_url)
    ActiveCall.create('agent1', conference_id)
    print agent_sip, sip_numbers[0], sip_numbers[1]
    NumberConfig.create(agent_sip, sip_numbers[0], sip_numbers[1])
    return str(twiml_generator.generate_connect_conference(conference_id,
                                                           url_for('wait'),
                                                           True,
                                                           True))


def generate_token(agent_id):
    return jsonify(token=token.generate(agent_id), agentId=agent_id)


def call_agent(agent_id):
    dict = request.form
    for key in dict:
        print 'form key ', key, ' = ', dict[key]
    CallSid = request.form['CallSid']
    Called = request.form['Called']
    to_sip = request.form['To']
    from_ = request.form['From']
    print 'from_: ', from_
    from_numbers=from_.split(':')[1]
    from_sip = from_numbers.split('@')
    print 'to_sip: ', to_sip
    tosip=to_sip.split(':')[1]
    sip_ext = tosip.split('@')[0]
    to = sip_ext
    print 'sip_ext: ', sip_ext
    print 'sip_ext len: ', len(sip_ext)
    is_sip =  False
    if len(sip_ext) == 3:
        to =  'sip:' + tosip
        is_sip =  True
    else:
        from_ = NumberConfig.number_for(from_sip[0], from_sip[1])
        if sip_ext[:2] == "00": 
            to = tos[2:]
        if tosip[:3] == "011":
            to = tos[2:]
    
    print 'Last From: ', from_
    
    #tos = request.form['To'].split(':').split('@')
    #to = tos[1]
    print to, ' ', sip_ext
    
    conference_id = ActiveCall.conference_id_for(agent_id)
    print 'conference_id: ', conference_id
    connect_agent_url = url_for('connect_agent', agent_id='agent2',
                                conference_id=conference_id, _external=True)
    #call.call_agent(from_, to, 'http://demo.twilio.com/docs/voice.xml')
    return str(twiml_generator.generate_call_agent(from_, to, AGENT_WAIT_URL, is_sip))
    #return str(twiml_generator.generate_connect_conference(conference_id,
    #                                                       AGENT_WAIT_URL,
    #                                                       True,
    #                                                       True))


def wait():
    return str(twiml_generator.generate_wait())


def connect_agent(conference_id, agent_id):
    exit_on_end = True #'agent2' == agent_id
    return str(twiml_generator.generate_connect_conference(conference_id,
                                                           AGENT_WAIT_URL,
                                                           True,
                                                           exit_on_end))
