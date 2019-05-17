from twilio.rest import Client
from os import environ as ENV


def call_agent(from_, agent_id, callback_url):
    account_sid = ENV['TWILIO_ACCOUNT_SID']
    auth_token = ENV['TWILIO_AUTH_TOKEN']
    my_number = ENV['TWILIO_NUMBER']
    client = Client(account_sid, auth_token)

    #to = 'client:' + agent_id
    to = agent_id
    #from_ = my_number
    if 'sip:' in from_:
        from_numbers=from_.split(':')[1]
        from_ = from_numbers.split('@')[0]
    
    print 'from_number: ', from_
    call = client.calls.create(to, from_, url=callback_url)
    print to, '-', from_,'-',callback_url
    return call.sid
