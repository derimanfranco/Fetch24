import json
import urllib2
import datetime

# Last 24 hours collector

def get_headers(token):
    """
    Prepares the CURL headers
    :return:
    """
    # Prepare the arguments of the call
    headers = dict()
    headers['Accept'] = 'application/json; application/vnd.esios-api-v1+json'
    headers['Content-Type'] = 'application/json'
    headers['Host'] = 'api.esios.ree.es'
    headers['Authorization'] = 'Token token=\"' + token + '\"'
    headers['Cookie'] = ''
    return headers


def get_data(token,indicator=1013):
    """
    Get json file with the tariff for today.
    The indicators are the indexes assigned to the available data series
    :return:
    """
    # indicator=1013 by default
    varnow=datetime.datetime.utcnow()
    print 'Actual date\t' + str(varnow)

    # Desfase debido a la hora peninsular UTC+1
    start=varnow.replace(hour=00) - datetime.timedelta(hours=1)
    end=start + datetime.timedelta(hours=24)

    print '\tSince\t'+str(start) +'\n\t to \t'+ str(end)

    url = 'https://api.esios.ree.es/indicators/' + str(indicator) + '?start_date=' + str(start) + '&end_date=' + str(end)+'&time_trunc=hour'

    req = urllib2.Request(url, headers=get_headers(token))
    response = urllib2.urlopen(req)
    try:
        json_data = response.read().decode('utf-8')
    except:
        json_data = response.readall().decode('utf-8')

    result = json.loads(json_data)

    return result


if __name__ == '__main__':
    """
    main function
    Print price
    """
    file = open('esios_token','r')
    esios_token=file.readline()

    result=get_data(esios_token)

    for timeslot in result['indicator']['values']:
        print(timeslot)


