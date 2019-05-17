from twilio.twiml.voice_response import VoiceResponse, Dial

from os import environ as ENV

def generate_wait():
    twiml_response = VoiceResponse()
    wait_message = 'Thank you for calling. Please wait in line for a few seconds. An agent will be with you shortly.'
    wait_music = 'http://com.twilio.music.classical.s3.amazonaws.com/BusyStrings.mp3'
    twiml_response.say(wait_message)
    twiml_response.play(wait_music)
    return str(twiml_response)


def generate_connect_conference(call_sid, wait_url, start_on_enter, end_on_exit):
    twiml_response = VoiceResponse()
    dial = Dial()
    dial.conference(call_sid,
                    start_conference_on_enter=start_on_enter,
                    end_conference_on_exit=end_on_exit,
                    wait_url=wait_url)
    res = str(twiml_response.append(dial))
    print 'generate_connect_conference'
    print res
    return res

def generate_call_agent(from_, agent_id, callback_url, is_sip =  False):
    account_sid = ENV['TWILIO_ACCOUNT_SID']
    auth_token = ENV['TWILIO_AUTH_TOKEN']
    my_number = ENV['TWILIO_NUMBER']
    #from_ = my_number
    #from_ = my_number
    if 'sip:' in from_:
        from_numbers=from_.split(':')[1]
        from_ = from_numbers.split('@')[0]
    twiml_response = VoiceResponse()
    dial = Dial(caller_id=from_)
    if is_sip:
        dial.sip(agent_id)
    else:
        dial.number(agent_id)
    twiml_response.append(dial)
    res = str(twiml_response)
    print res
    return res
